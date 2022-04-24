import os
import csv
from time import time
from random import choice
from PIL import ImageTk, Image
from tkinter import Tk, Canvas, Label, Button, StringVar, OptionMenu, Checkbutton, IntVar

#Other Files
from Unistroke import Unistroke
from Steps import Steps

##############################################################################################################################################################################################
#GUI Components
root = Tk()
canvas = Canvas(root, bg='black')
label = Label(root, width=50, bg = 'yellow')
isProtractor = False
#Lists to store User stroke
user_points, temp_points, timestamps, user_vectors = [], [], [], []

##############################################################################################################################################################################################
###TEMPLATES PREPROCESSING PART
unistroke = Unistroke()
templates = unistroke.GetTemplatesProtractor() if isProtractor else unistroke.GetTemplates()

##############################################################################################################################################################################################
###GUI PART

#To Clear Canvas
def clear():
    user_points, timestamps = [], []
    canvas.delete('all')
    label.configure(text = "\n")

#To get the first coordinate
def start(event):
    clear()
    global X, Y, temp_points, timestamps
    X, Y, z = event.x, event.y, 4.5
    timestamps.append(int(time()))
    canvas.create_rectangle(X-z, Y-z, X+z, Y+z, fill = "white", width = 1)
    temp_points.append([X, Y])
    label.configure(text = "\n")

#To draw the stroke
def draw(event):
    global X, Y, temp_points, timestamps
    canvas.create_line((X, Y, event.x, event.y), fill = 'white', width = 3)
    X, Y = event.x, event.y
    temp_points.append([X, Y]) #points are saved here one by one
    timestamps.append(time())

#Check if the user finished the stroke and save the points
def on_release(event):
    global temp_points, points
    #forgetAll()
    global b7
    b7.pack_forget()
    str1, str2='',''
    b7 = Button(root, text="Show Process", border=5, command=lambda: Steps().show(str1, str2, unistroke.GetTemplates(),unistroke.GetTemplatesProtractor()))
    global b3
    b3.pack_forget()
    b3.pack(side="left",padx=15)
    b7.pack(side="right",padx=15)

    #Check if minimum number of points were made
    if len(temp_points) >= 5:
        user_points = (temp_points).copy() #all the points are copied for further steps.
        temp_points = []
        #Calling recognize function
        steps = Steps()
        #shape, score, time_taken = steps.recognize(user_points, user_vectors,templates, True, True) if isProtractor else steps.recognize(user_points, user_vectors,templates,True)
        shape, score, time_taken = steps.recognize(user_points, user_vectors,unistroke.GetTemplates(), True)
        #Formatting
        score = str("{:.3f}".format(score))
        time_taken = str("{:.3f}".format(time_taken*1000))
        str1 = shape + " (" + score + ") in " + time_taken + " ms"
        label["text"] = "$1 Result: " + str1
        shape, score, time_taken = steps.recognize(user_points, steps.Vectorize(user_points),unistroke.GetTemplatesProtractor(), True, True)
        #Formatting
        score = str("{:.3f}".format(score))
        time_taken = str("{:.3f}".format(time_taken*1000))
        str2 = shape + " (" + score + ") in " + time_taken + " ms"
        label["text"] += "\n Protractor: " + str2
        #steps.show(str1, str2)


    else:
        label["text"] = "Too few points made. Please try again."

##############################################################################################################################################################################################
###OFFLINE PROCESSING
#To read the XML Files
def xmlParser( bspath = 'xml/xml_logs/', sub = '/medium/', extra = ''):
    basepath = bspath
    flag = False
    f=[]
    g=[]
    users, gestures = [],[]

    for entry in os.listdir(basepath):
        if flag or bspath != 'xml/xml_logs/':
            #store user names
            users.append(str(entry))

            basepath += str(entry)
            basepath += sub
            S=[]
            NumPts, Speed = [],[]
            for fileEntry in os.listdir(basepath):
                #store gesture names
                if fileEntry[:-6] not in gestures:
                    gestures.append(fileEntry[:-6])

                lines = open(basepath+str(fileEntry), "r")
                i=0
                givenLabel=''
                givenPoints = []
                for line in lines:

                    if bspath != 'xml/xml_logs/':
                        if i==0:
                            words = (line.split()[-2:])
                            NumPts.append(int(words[0][8:-1]))
                            Speed.append(float(words[1][14:-2]))
                    else:
                        if i==1:
                            words = (line.split()[5:7])
                            NumPts.append(int(words[0][8:-1]))
                            Speed.append(float(words[1][13:-1]))

                    if i==1 and line!= '</Gesture>'+extra:
                        words = (line.split())[1]
                        givenLabel = words[6:-3]
                    elif i>1 and line!= '</Gesture>'+extra:
                        xc,yc = 0,0
                        lineword = line.split()
                        xc, yc = lineword[1], lineword[2]
                        xc, yc = xc.replace('X="',''), yc.replace('Y="','')
                        xc, yc = xc.replace('"',''), yc.replace('"','')

                        givenPoints.append([int(xc),int(yc)])

                    i+=1

                S.append([givenLabel, givenPoints, str(entry)+'-'+str(fileEntry[:-4])])
                f.append(S)
                g.append([NumPts, Speed])
                S=[]
                NumPts, Speed = [],[]
            basepath = bspath
        flag=True
    return(f, users, gestures, g)

#Code to implement OFFLINE RECOGNITION
def offlineRecognizer(points, user_vectors, givenLabels, givenNames, users, gestures, LoadCustomDataset, NumPts, Speeds):
    progress = 0
    global isProtractor
    time0 = time()
    nextSet = 0
    file = open('logfile.csv', 'w', newline='')
    writer = csv.writer(file)
    TotalAvgScore, TotalAvgTime = 0, []
    steps = Steps()
    writer.writerow(['Recognition Log: [SRI CHAITANYA NULU] // [$1 RECOGNITIION ALGORITHM] // [USERS GESTURES XML DATASET] // USER-DEPENDENT RANDOM-100'])
    writer.writerow(['User[all-users]','GestureType[all-gestures-types]','RandomIteration[1to100]','#ofTrainingExamples[E]','TotalSizeOfTrainingSet[count]','TrainingSetContents[specific-gesture-instances]','Candidate[specific-instance]','NumPts', 'Speed', 'RecoResultGestureType[what-was-recognized]','CorrectIncorrect[1or0]','RecoResultScore','RecoResultBestMatch[specific-instance]','Recognition Time (in Milliseconds)', 'RecoResultNBestSorted[instance-and-score]'])
    for U in range(1,len(users)+1):
        time1 = time()
        Score = []
        #To store the row
        entry = [[]]*16
        #User Name
        entry[1] = str(users[U-1])

        for E in range(1, 10):

            timeE1 = time()
            #Number of Training Examples
            entry[4] = str(E)

            #Total number of training set elements
            entry[5] = str(E*len(gestures))

            for itr in range(1, 101):
                #Iteration Number
                entry[3] = str(itr)
                Candidates, Candidates_Names, Candidates_Vectors = [], [], []
                CandidateNumPts, CandidateSpeeds = [], []
                gest, Templates = [], []
                step = -10
                for G in range(1,17):
                    #Gesture
                    gest.append(str(gestures[G-1]))

                    step+=10
                    R= [i for i in range(1+step,10+step+1)]

                    #Choosing Templates
                    for i in range(0,E):
                        r = choice(R)
                        R.remove(r)
                        Templates.append([givenNames[nextSet+r-1], points[nextSet+r-1][1], steps.Vectorize(points[nextSet+r-1][1])])
                    r = choice(R)
                    Candidates_Names.append(givenNames[nextSet+r-1])
                    Candidates.append(points[nextSet+r-1][1])
                    CandidateNumPts.append(NumPts[nextSet+r-1])
                    CandidateSpeeds.append(Speeds[nextSet+r-1])


                #Set of Templates
                entry[6] = '{'+', '.join([i[0] for i in Templates])+'}'

                cn = 0
                for c in Candidates:

                    #gesture
                    entry[2] = gest[cn]
                    #Candidate
                    entry[7] = Candidates_Names[cn]
                    entry[8] = CandidateNumPts[cn][0]
                    entry[9] = CandidateSpeeds[cn][0]
                    steps = Steps()
                    Tt1, Tt2 = 0, 0

                    if not isProtractor:
                        #print('NotProtractor')
                        Tt1 = time()
                        shape, score, scores = steps.recognize(c, [],Templates, False)
                        Tt2 = time()
                    else:
                        Tt1 = time()
                        #print('Protractor')
                        shape, score, scores = steps.recognize(c, steps.Vectorize(c), Templates, False, True)
                        Tt2 = time()
                    entry[14] = (Tt2-Tt1)*1000
                    TotalAvgTime.append(entry[14])

                    #Gesture Recognized
                    entry[10] = shape[3:-2] if LoadCustomDataset else shape[4:-2]

                    if shape[:-2] == entry[7][:-2]:
                        entry[11] = '1'
                        Score.append(1)

                    else:
                        entry[11] = '0'
                        Score.append(0)

                    entry[12] = str("{:.3f}".format(score))
                    entry[13] = shape
                    entry[15] = '{'+str(scores)+'}'
                    cn+=1
                    progress+=1


                    #writing the entry to the log file
                    writer.writerow(entry[1:])
                label["text"] = '\nOffline Recognition is running...\nDo not close this window...\n\nDetails:\n--------\nUser: '+str(U)+'/'+str(len(users))+'\n'+ 'E value: '+str(E)+'/9\nIteration: '+str(itr)+'/100\nProgress: ' + str("{:.2f}".format(((progress/(16*9*len(users)*100))*100)))+'%\n'
                root.update()

        nextSet+=160
        TotalAvgScore += sum(Score)/len(Score)
        time2 = time()
        #print('U', U, time2-time1)
    #print('total:', time()-time0)
    writer.writerow([])
    writer.writerow(['Total Average Score',str("{:.3f}".format(TotalAvgScore/U))])
    writer.writerow(['Total Average Time',str("{:.3f}".format(sum(TotalAvgTime)/len(TotalAvgTime)))+ 'ms'])
    return [str("{:.4f}".format(TotalAvgScore/U)), str("{:.4f}".format(sum(TotalAvgTime)/len(TotalAvgTime)))+ 'ms']

def offline( LoadCustomDataset = False):
    Labels=[]
    Names=[]
    NumPts, Speeds = [], []
    global isProtractor
    f, users, gestures, g = xmlParser('User Gesture Dataset/', '/','\n') if LoadCustomDataset else xmlParser()

    for i in range(0, len(f)):
        steps = Steps()
        name, points, vector = steps.GetTemplate("", f[i][0][1], isProtractor)
        user_points.append([name, points])
        user_vectors.append(vector)
        Labels.append(f[i][0][0])
        Names.append(f[i][0][2])
        NumPts.append(g[i][0])
        Speeds.append(g[i][1])

    acc, tim = offlineRecognizer(user_points, user_vectors, Labels, Names, users, gestures, LoadCustomDataset, NumPts, Speeds)
    b3.pack()

    label["text"] += "\nAll Tasks Completed...\nLog file saved in the current directory\n\nAccuracy:"+acc+"\n\nTime:"+tim+"\n\nSelect 'back' to go to main screen\n"



##############################################################################################################################################################################################
###CUSTOM USERS DATASET CREATION

#success message + endscreen
def endscreen(msg = '\nSuccess!!\nAll the data has been stored.\nThank you for providing samples.\n'):
    forgetAll()
    label1['font'] = 'Courier 13 bold'
    label1['text'] = msg
    label1['bg'] = 'yellow'
    label1.pack()
    l1.pack()
    b3.pack()
    l2.pack()

GestureSamples, Timestamps = [[]]*16, [[]]*16

#write to xml file
def savePoints():
    endscreen('Please wait...\nThe data is being saved...\n')
    path = 'User Gesture Dataset/S0'
    loc = ''
    file_count=0
    if not os.path.exists(path):
        os.makedirs(path)
        loc = path
    else:
        path, dirs, files = next(os.walk("User Gesture Dataset/"))
        file_count = len(dirs)
        os.makedirs('User Gesture Dataset/S'+str(file_count))
        loc = 'User Gesture Dataset/S'+str(file_count)



    j=0
    for G,T in zip(GestureSamples, Timestamps):
        i = 1
        for g,t in zip(G, T):
            st = templates[j][0]+'0'+str(i) if i<10 else templates[j][0]+str(i)
            f = open(loc+'/'+templates[j][0]+st+'.xml', 'w')

            if len(g[0])==2:
                f_line = '<Gesture Name="'+st+'" User="'+str(file_count)+'" Number="'+str(i)+'" NumPts="'+str(len(g))+'" Milliseconds="'+str("{:.3f}".format((t[len(t)-1]-t[0])*1000))+'">\n'
                f.write(f_line)

                for x,z in zip(g,t):

                    f.write('<Point X="'+str(x[0])+'" Y="'+str(x[1])+'" T="'+str("{:.3f}".format((z)))+'"/>\n')
            else:
                f_line = '<Gesture Name="'+st+'" User="'+str(file_count)+'" Number="'+str(i)+'" NumPts="'+str(len(g[0]))+'" Milliseconds="'+str("{:.3f}".format((t[0][len(t[0])-1]-t[0][0])*1000))+'">\n'
                f.write(f_line)

                for x,z in zip(g[0],t[0]):
                    f.write('<Point X="'+str(x[0])+'" Y="'+str(x[1])+'" T="'+str("{:.3f}".format((z)))+'"/>\n')

            f.write('</Gesture>\n')
            i+=1
            if i== 11: i=1
        j+=1
        if j==16: j = 0

    endscreen()

#createDataset

def add():
    global temp_points, timestamps
    if len(temp_points)>5:
        clear()
        t=0
        index = 0
        temp, temptimes = [], []
        m = 10
        while t<len(templates):
            if variable.get() == templates[t][0]:
                index = t

                if len(GestureSamples[t]) < m:
                    sampleNum[index]+=1
                    noteLabel['text'] = 'Sample #'+str(sampleNum[index])
                    root.update()
                    temp.append([tp for tp in temp_points])
                    temptimes.append([ts for ts in timestamps])
                    temp_points, timestamps=[],[]
                    if len(GestureSamples[index]) == 0:
                        GestureSamples[index], Timestamps[index] = temp, temptimes
                    else:
                        GestureSamples[index].append(temp)
                        Timestamps[index].append(temptimes)

                if len(GestureSamples[t])==m and len(shapestr)>1:

                    noteLabel['text'] = '\nAll 10 samples for "'+variable.get()+'" collected.\nChoose another gesture.\n'

                    canvas.pack_forget()

                    noteLabel.pack_forget()
                    b5.pack_forget()
                    b6.pack_forget()
                    l1.pack_forget()
                    image.pack_forget()
                    l2.pack_forget()
                    l4.pack_forget()
                    shapestr.remove(variable.get())
                    label1['text']='\nMore '+str(len(shapestr))+' gestures left...\n'
                    global w
                    w.pack_forget()
                    w = OptionMenu(root, variable, *shapestr, command=option_changed)

                    l1.pack()
                    image.pack()
                    l2.pack()
                    w.pack()
                    l4.pack()
                    noteLabel.pack()
                    root.update()


                    break


            t+=1

        gsum=0

        for g in GestureSamples:
            gsum+=len(g)

        if gsum == m*16:
            savePoints()
    else:
        if len(noteLabel['text'])<=10:
            noteLabel['text'] += '\nToo few points made. Please try again.'


##############################################################################################################################################################################################
###OFFLINE PROCESSING ON THE CUSTOM USERS DATASET

def LoadCustomDataset():
    #Change the GUI
    forgetAll()
    label.pack(side = "top", fill = "x")
    label["font"] = "Courier 11 bold"
    label["text"]="\nOffline Recognition is running...\nDo not close this window...\n"
    #Using existing offline function on Custom Dataset

    offline(True)


##############################################################################################################################################################################################
###SOME MORE GUI HANDLING TO SWITCH BETWEEN SCREENS

#Helper function to remove GUI Elements
def forgetAll():
    label["text"] = "\n\n"
    label1["text"] = ""
    clear()
    label1.pack_forget()
    image.pack_forget()
    w.pack_forget()
    title.pack_forget()
    b1.pack_forget()
    l1.pack_forget()
    b2.pack_forget()
    l2.pack_forget()
    b2b.pack_forget()
    l2b.pack_forget()
    b4.pack_forget()
    l4.pack_forget()
    label.pack_forget()
    canvas.pack_forget()
    b3.pack_forget()
    b5.pack_forget()
    b6.pack_forget()
    noteLabel.pack_forget()
    b7.pack_forget()
    c1.pack_forget()
    newlabel.pack_forget()

#To go back to main screen
def back():
    forgetAll()
    #Dataset creation GUI
    global photo, image, variable, shapestr, user_points, temp_points, timestamps, GestureSamples, Timestamps,w, sampleNum
    photo = ImageTk.PhotoImage(Image.open('Gestures/'+'logo'+'.png'))
    image = Label(root, image = photo)
    variable = StringVar(root)
    shapestr = ['triangle', 'x', 'rectangle', 'circle', 'check', 'caret'
                        , 'zigzag', 'arrow', 'left_square_brace', 'right_square_brace', 'v', 'delete',
                   'left_curly_brace', 'right_curly_brace', 'star', 'pigtail']
    user_points, temp_points, timestamps = [], [], []
    GestureSamples, Timestamps = [[]]*16, [[]]*16
    w = OptionMenu(root, variable, *shapestr, command=option_changed)
    sampleNum = [1]*16
    label["bg"] = "yellow"
    label.pack(side = "top", fill = "x")
    title.pack()
    b1.pack()
    l1.pack()
    c1.pack()
    newlabel.pack()
    b2.pack()
    l2.pack()
    b2b.pack()
    l2b.pack()
    b4.pack()
    l4.pack()
    label.pack(side = "top", fill = "x")
    label1['text'] = 'By N.S.Chaitanya'
    label1.pack()

#Live Recognition
def liveGUI():
    forgetAll()
    label.pack(side = "top", fill = "x")
    canvas.pack(anchor = 'nw', fill = 'both', expand = 1)
    canvas.bind("<Button-1>", start)
    canvas.bind("<B1-Motion>", draw)
    canvas.bind("<ButtonRelease-1>", on_release)
    b3.pack()

#Offline Recognition
def offlineGUI(LoadCustomDataset = False):
    forgetAll()
    label.pack(side = "top", fill = "x")
    label["font"] = "Courier 11 bold"
    label["text"]="\nOffline Recognition is running...\nDo not close this window...\n"
    root.after(100, offline, (LoadCustomDataset))


#Dataset creation GUI
photo = ImageTk.PhotoImage(Image.open('Gestures/'+'logo'+'.png'))
image = Label(root, image = photo)
variable = StringVar(root)
shapestr = ['triangle', 'x', 'rectangle', 'circle', 'check', 'caret'
                    , 'zigzag', 'arrow', 'left_square_brace', 'right_square_brace', 'v', 'delete',
               'left_curly_brace', 'right_curly_brace', 'star', 'pigtail']



#code to change UI when a gesture is selected
sampleNum = [1]*16
def option_changed(self):
    global image, variable,photo

    forgetAll()
    photo = ImageTk.PhotoImage(Image.open('Gestures/'+variable.get()+'.png'))
    image = Label(root, image = photo)
    label1['text'] = '\nYou can press clear to clean the canvas.'
    label1['text'] += '\nor\nJust draw a new stroke.\n\nCanvas is cleared automatically when you add.\n'
    label1['text'] += '\nIf you get tired of drawing the same gesture,\nuse the dropdown menu to change them.\n'
    label1.pack()
    l1.pack()
    image.pack()
    l2.pack()
    global w
    w.pack_forget()
    w = OptionMenu(root, variable, *shapestr, command=option_changed)
    w.pack()
    num=0
    while num < len(templates):
        if variable.get()==templates[num][0]:
                   break
        num+=1

    noteLabel['text'] = 'Sample #'+str(sampleNum[num])
    canvas.bind("<Button-1>", start)
    canvas.bind("<B1-Motion>", draw)
    canvas.unbind("<ButtonRelease-1>")
    canvas.pack(anchor = 'nw', fill = 'both', expand = 1)

    noteLabel.pack()
    b5.pack(side='left', padx=50)
    b6.pack(side='right', padx=50)
    l4.pack()

#GUI for creating dataset
w = OptionMenu(root, variable, *shapestr, command=option_changed)
def createDatasetGUI():
    forgetAll()
    label1['text'] = '\nPick a gesture and follow instructions!\nThere are 16 gestures to draw.\n Each gesture needs 10 samples.\n'
    label1['bg'] = 'yellow'
    label1.pack()

    l1.pack()
    variable.set("Click here to select a gesture")

    w.config(font='Courier 10 bold')
    image.pack_forget()
    w.pack_forget()
    image.pack()
    l2.pack()
    w.pack()
    l4.pack()
    b3.pack()
    root.mainloop()

##############################################################################################################################################################################################
###

def protractorEnable():
    if var.get()==1:
        global isProtractor
        isProtractor = True
    else:
        isProtractor = False

##############################################################################################################################################################################################
###MAIN FUNCTION

title = Label(root, text='\nChoose an Option:\n', font="Courier 13 bold underline")
b1 = Button(root, text="Click here for Live Recognition", border=5, command=liveGUI)
l1 = Label(root, text='\n')
b2 = Button(root, text="Click here for Offline Recognition", border=5, command=offlineGUI)
l2 = Label(root, text='\n')
b2b = Button(root, text="Click here for Offline Recognition on Custom User Dataset", border=5, command=lambda: offlineGUI(True))
l2b = Label(root, text='\n')
b4 = Button(root, text="Click here to add gestures for the dataset", border=5, command=createDatasetGUI)
l4 = Label(root, text='\n')
b3 = Button(root, text="Back", border=5, command=back)
b5 = Button(root, text="Clear", border=5, command=clear)
b6 = Button(root, text="Add", border=5, command=add)
b7 = Button(root, text="Show Process", border=5)
var = IntVar()
c1 = Checkbutton(root, text='Enable Protractor For Offline Recgonition',variable=var, onvalue=1, offvalue=0, command=protractorEnable)
newlabel = Label(root, text='\n')
label1 = Label(root, width=50, bg = 'yellow', font = 'Courier 11 bold')
noteLabel = Label(root, width=50, bg = 'yellow', font = 'Courier 11 bold')

#Starts the Program
def main():
    root.resizable(0,0)
    root.title("$1 Recognizer + Protractor")
    label['font'] = 'Courier 10 bold'
    label.pack(side = "top", fill = "x")
    title.pack()
    b1.pack()
    l1.pack()
    c1.pack()
    newlabel.pack()
    b2.pack()
    l2.pack()
    b2b.pack()
    l2b.pack()
    b4.pack()
    l4.pack()
    label.pack(side = "top", fill = "x")
    label1['text'] = 'By N.S.Chaitanya'
    label1.pack()
    root.mainloop()

#Calling Main Function
main()

##############################################################################################################################################################################################
