from math import dist,atan2,cos,sin,radians,sqrt, atan, acos, pi, floor
from time import time
import matplotlib.pyplot as plt

#Constants
N=64
sqr_size = 250.0
origin = [0, 0]
angle_range = radians(45)
angle_incr = radians(2)
phi = 0.5 * (-1.0 + sqrt(5.0))

Default, Resampled, Rotated, Scaled, Translated = [],[],[],[],[]
DefaultP, ResampledP, VectorizedP = [],[],[]
template_final, template_finalP= [], []
template_final_index, template_finalP_index = 0, 0

#Process the Template points
class Steps:

    def GetTemplate(self, name, points, isProtractor = False):

        Vector = []
        steps = Steps()
        Name = name
        global N, Default, Resampled, Rotated, Scaled, Translated, DefaultP, ResampledP, VectorizedP
        if isProtractor==False:
            if name=="":
                lx,ly=[],[]
                for x,y in points:
                    lx.append(x)
                    ly.append(y)
                Default=[]
                Default.append([lx,ly])

            ###Resampling###
            Points = self.resample(points, N)

            if name=="":
                lx,ly=[],[]
                for x,y in Points:
                    lx.append(x)
                    ly.append(y)
                Resampled=[]
                Resampled.append([lx,ly])

            ###Roatate To Zero###
            Points = self.rotateToZero(Points)

            if name=="":
                lx,ly=[],[]
                for x,y in Points:
                    lx.append(x)
                    ly.append(y)
                Rotated=[]
                Rotated.append([lx,ly])

            ###Scale To Square###
            Points = self.scaleToSquare(Points, sqr_size)

            if name=="":
                lx,ly=[],[]
                for x,y in Points:
                    lx.append(x)
                    ly.append(y)
                Scaled=[]
                Scaled.append([lx,ly])

            ###Translate To Origin###
            Points = self.translateToOrigin(Points, origin)
            if name=="":
                lx,ly=[],[]
                for x,y in Points:
                    lx.append(x)
                    ly.append(y)
                Translated=[]
                Translated.append([lx,ly])

        else:
            n = 16
            if name=="":
                lx,ly=[],[]
                for x,y in points:
                    lx.append(x)
                    ly.append(y)
                DefaultP=[]
                DefaultP.append([lx,ly])

            ###Resampling###
            Points = self.resample(points, n)
            if name=="":
                lx,ly=[],[]
                for x,y in Points:
                    lx.append(x)
                    ly.append(y)
                ResampledP=[]
                ResampledP.append([lx,ly])

            ###Vectorizing###
            Vector = self.Vectorize(Points)

            if name=="":
                VectorizedP = Vector

        return [name, Points, Vector]

    ###HELPER FUNCTIONS

    ##To find the centroid of all the points given
    #(Used in Step-2 and Step-3)
    def centroid(self, points):
        sumx, sumy, i = 0.0, 0.0, 0
        while(i < len(points)):
            sumx += points[i][0]
            sumy += points[i][1]
            i += 1
        cx, cy = sumx/len(points), sumy/len(points)
        return cx, cy

    ##To find the bounding box for the given list of points.
    #Returns a dictionary with x, y, width and height.
    #(Used in Step-3)
    def boundingBox(self, points):
        i, minX, maxX, minY, maxY = 0, float('inf'), -float('inf'), float('inf'), -float('inf')
        while i < len(points):
            minX, maxX = min(minX, points[i][0]), max(maxX, points[i][0])
            minY, maxY = min(minY, points[i][1]), max(maxY, points[i][1])
            i+=1
        return {'x': minX, 'y': minY, 'width': maxX - minX, 'height': maxY - minY}


    ##############################################################################################################################################################################################
    ###STEP-1
    def pathLength(self, A):
        d = 0.0
        for i in range(0, len(A)):
            d += dist(A[i-1], A[i])
        return d

    def resample(self, points, n):

        I = self.pathLength(points) / float(n-1)
        D = 0.0
        newPoints = [points[0]]
        i = 1
        while i < len(points):
            d = dist(points[i-1], points[i])
            if D + d >= I:
                    qx = points[i-1][0] + float((I-D)/d) * (points[i][0] - points[i-1][0])
                    qy = points[i-1][1] + float((I-D)/d) * (points[i][1] - points[i-1][1])
                    newPoints.append([qx,qy])
                    points.insert(i, [qx,qy])
                    D = 0.0
            else:
                    D += d
            i += 1
        while len(newPoints) < n:
                newPoints.append(points[len(points) - 1])
        return newPoints


    ##############################################################################################################################################################################################
    ###STEP-2

    def rotateBy(self, points, theta):
        cx, cy = self.centroid(points)
        cosine = cos(theta)
        sine = sin(theta)
        newpoints = []
        i = 0
        while i < len(points):
            qx=(points[i][0] - cx) * cosine - (points[i][1] - cy) * sine + cx
            qy=(points[i][0] - cx) * sine + (points[i][1] - cy) * cosine + cy
            newpoints.append([qx, qy])
            i += 1
        return newpoints

    def rotateToZero(self, points):
        cx, cy = self.centroid(points)
        theta = atan2(cy - points[0][1], cx - points[0][0])
        newPoints = self.rotateBy(points, -theta)
        return newPoints


    ##############################################################################################################################################################################################
    ###STEP-3

    def scaleToSquare(self, points, size):
        b = self.boundingBox(points)
        newpoints = []
        i = 0
        while i < len(points):
            qx = points[i][0] * (size / b['width'])
            qy = points[i][1] * (size / b['height'])
            newpoints.append([qx, qy])
            i += 1
        return newpoints

    def translateToOrigin(self, points, pt):
        cx, cy = self.centroid(points)
        newpoints = []
        i=0
        while i < len(points):
            qx = points[i][0] + pt[0] - cx
            qy = points[i][1] + pt[1] - cy
            newpoints.append([qx, qy])
            i += 1
        return newpoints


    ##############################################################################################################################################################################################
    ###STEP-4

    def pathDistance(self, A, B):
        d = 0
        i = 0
        while i < len(A):
            d = d + dist(A[i], B[i])
            i += 1
        return d / len(A)

    def distanceAtAngle(self, points, template, theta):
        newPoints = self.rotateBy(points, theta)
        d = self.pathDistance(newPoints, template[1])
        return d

    def distanceAtBestAngle(self, points, template, A, B, delta):
        x1 = phi * A + (1 - phi) * B
        f1 = self.distanceAtAngle(points, template, x1)
        x2 = (1 - phi) * A + phi * B
        f2 = self.distanceAtAngle(points, template, x2)
        while abs(B - A) > delta:
            if f1 < f2:
                    B, x2, f2 = x2, x1, f1
                    x1 = phi * A + (1 - phi) * B
                    f1 = self.distanceAtAngle(points, template, x1)
            else:
                    A, x1, f1 = x1, x2, f2
                    x2 = (1 - phi) * A + phi * B
                    f2 = self.distanceAtAngle(points, template, x2)
        return min(f1, f2)


##############################################################################################################################################################################################
###Protractor Specific Functions

    def Vectorize(self, points):
        cx, cy = self.centroid(points)
        points = self.translateToOrigin(points,origin)
        indicativeAngle = atan2(points[0][1], points[0][0])
        #delta = ((pi / 4) * floor((indicativeAngle + pi / 8) / (pi / 4)))-indicativeAngle for orientation sensitive
        delta = -indicativeAngle
        sum = 0
        vector = []
        for x,y in points:
            newX =  (x * cos(delta)) - (y * sin(delta))
            newY =  (y * cos(delta)) + (x * sin(delta))
            vector.append(newX)
            vector.append(newY)
            sum += ((newX*newX) + (newY*newY))
        magnitude = sqrt(sum)
        for i in range(0, len(vector)):
            vector[i] = vector[i]/magnitude
        return vector

    def OptimalCosineDistance(self, v1, v2):
        a,b = 0,0
        for i in range(0, len(v1)-1,2):
            a += v1[i]*v2[i] + v1[i+1]*v2[i+1]
            b += v1[i]*v2[i+1] - v1[i+1]*v2[i]
        angle = atan(b/a)
        #can be divided by pi to normalize, but not required.
        return (acos(a*cos(angle)+b*sin(angle))/pi)


##############################################################################################################################################################################################
###Recognition

    def recognize(self, Points, vector, templates, flag=True, isProtractor = False):

        global template_final,template_finalP, final_Points, final_Vector
        global template_final_index, template_finalP_index

        start_time = time()
        #Process the points
        if flag:
            Name, Points, vector = self.GetTemplate("", Points, isProtractor)

        #start the recognititon process
        b = float('inf')
        selected_template = None
        scores, vals = [], []
        index = 0
        for template in templates:
            d = 0
            if isProtractor:
                d = self.OptimalCosineDistance((template[2]), vector)
            else:
                d = self.distanceAtBestAngle(Points, template, -angle_range, angle_range, angle_incr)
            if d < b:
                b = d
                selected_template = template[0]
                if not isProtractor:
                    template_final = template[1]
                    template_final_index = index
                else:
                    template_finalP = template[2]
                    template_finalP_index = index
            if flag==False:
                if isProtractor:
                    scores.append(template[0]+': '+str("{:.2f}".format(1 - d)))
                    vals.append(1 - d)
                else:
                    scores.append(template[0]+': '+str("{:.2f}".format(1 - d / (0.5 * sqrt(sqr_size ** 2 + sqr_size ** 2)))))
                    vals.append(1 - d / (0.5 * sqrt(sqr_size ** 2 + sqr_size ** 2)))
            index+=1

        score = 1 - (b / (0.5 * sqrt(sqr_size ** 2 + sqr_size ** 2))) if not isProtractor else (1 - b)
        end_time = time()
        #Check if none of the templates match
        if selected_template == None:
            return ["No match.", 0.0, end_time - start_time]
        sortedScores = [scores for _,scores in sorted(zip(vals,scores), reverse=True)]

        return [selected_template, score, end_time-start_time] if flag else [selected_template, score, ', '.join(sortedScores)]

##############################################################################################################################################################################################
###Function To Plot The Steps

    def show(self, str1, str2, l1, l2):
        global Default, Resampled, Rotated, Scaled, Translated, Vectorized, DefaultP, ResampledP, VectorizedP, template_final, template_finalP
        fig, axs = plt.subplots(2, 3, sharex=True, sharey=True)

        axs[0, 0].scatter(Default[0][0], Default[0][1], s =[3])
        axs[0, 0].set_title('1. Original Points')
        axs[0, 0].invert_yaxis()
        axs[0, 0].set_aspect('equal', adjustable=None)


        axs[0, 1].scatter(Resampled[0][0], Resampled[0][1], s =[3], c = 'red')
        axs[0, 1].set_title('2. Resample')
        axs[0, 1].invert_yaxis()
        axs[0, 1].set_aspect('equal', adjustable=None)


        axs[0, 2].scatter(Rotated[0][0], Rotated[0][1], s =[3], c = 'green')
        axs[0, 2].set_title('3. Rotate')
        axs[0, 2].invert_yaxis()
        axs[0, 2].set_aspect('equal', adjustable=None)


        axs[1, 0].scatter(Scaled[0][0], Scaled[0][1], s =[3], c = 'magenta')
        axs[1, 0].set_title('4. Scale')
        axs[1, 0].invert_yaxis()
        axs[1, 0].set_aspect('equal', adjustable=None)

        axs[1, 1].scatter(Translated[0][0], Translated[0][1], s =[3])
        axs[1, 1].set_title('5. Translate')
        axs[1, 1].invert_yaxis()
        axs[1, 1].set_aspect('equal', adjustable=None)

        lx,ly = [],[]

        for x,y in template_final:
            lx.append(x)
            ly.append(y)

        axs[1, 2].set_aspect('equal', adjustable=None)
        axs[1, 2].scatter(Translated[0][0], Translated[0][1], s =[3])
        axs[1, 2].scatter(lx, ly, s=[3])
        axs[1, 2].set_title('6. Best Match:\n'+str1.capitalize())
        axs[1, 2].invert_yaxis()
        axs[1, 2].legend(["User Gesture", "Best Template"], loc ="lower right")


        fig.suptitle("$1 Recognizer Process",fontsize=24)
        plt.figtext(0.5, 0.01, "Press 'Alt+F4' to close window", ha="center", fontsize=12)
        plt.get_current_fig_manager().full_screen_toggle()
        plt.show()

        self.show_recognition(l1, False)


        fig, axs = plt.subplots(2, 2, sharex=False, sharey=False)

        axs[0, 0].scatter(DefaultP[0][0], DefaultP[0][1], s =[12])
        axs[0, 0].set_title('1. Original Points')
        axs[0, 0].invert_yaxis()
        axs[0, 0].set_aspect('equal', adjustable=None)

        axs[0, 1].plot(ResampledP[0][0], ResampledP[0][1], 'r:')
        axs[0, 1].scatter(ResampledP[0][0], ResampledP[0][1], s =[12])
        axs[0, 1].set_title('2. Resample')
        axs[0, 1].invert_yaxis()
        axs[0, 1].set_aspect('equal', adjustable=None)

        lx,ly = [],[]
        for i in range(0, len(VectorizedP)-1,2):
            lx.append(VectorizedP[i])
            ly.append(VectorizedP[i+1])
        axs[1, 0].plot(lx,ly, 'g:')
        axs[1, 0].scatter(lx, ly, s =[12], c = 'red')
        axs[1, 0].set_title('3. Vectorize')
        axs[1, 0].invert_yaxis()
        axs[1, 0].set_aspect('equal', adjustable=None)


        templx,temply=lx,ly
        axs[1, 1].scatter(lx,ly, s =[12])
        lx,ly = [],[]
        for i in range(0, len(template_finalP)-1,2):
            lx.append(template_finalP[i])
            ly.append(template_finalP[i+1])
        axs[1, 1].scatter(lx, ly, s =[12])
        axs[1, 1].legend(["User Gesture","Best Template"])
        axs[1, 1].plot(templx,temply, ':')
        axs[1, 1].plot(lx,ly, ':')
        axs[1, 1].set_title('4. Best Match:\n'+str2.capitalize())
        axs[1, 1].invert_yaxis()
        axs[1, 1].set_aspect('equal', adjustable=None)

        plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)

        fig.suptitle("$1+Protractor Recognizer Process",fontsize=24)
        plt.figtext(0.5, 0.01, "Press 'Alt+F4' to close window", ha="center", fontsize=12)
        plt.get_current_fig_manager().full_screen_toggle()
        plt.show()
        self.show_recognition(l2, True)

    def show_recognition(self, templatesList, isProtractor):
        #recognition
        #print(templatesList, len(templatesList))
        global template_final_index, template_finalP_index
        global Translated, VectorizedP

        fx,fy = [],[]
        if isProtractor==False:
            for x in Translated:
                fx.append(x[0])
                fy.append(x[1])
        else:
            for i in range(0, len(VectorizedP)-1, 2):
                fx.append(VectorizedP[i])
                fy.append(VectorizedP[i+1])

        i=0
        fig, axs = plt.subplots(4, 4, sharex=False, sharey=False)
        fig.suptitle("User Gesture Comparison with Templates",fontsize=24)
        plt.figtext(0.5, 0.01, "Red Points Represent Templates & Blue Points represent User Gesture\nPress 'Alt+F4' to close window", ha="center", fontsize=12)
        plt.get_current_fig_manager().full_screen_toggle()
        plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.4,
                    hspace=0.4)

        sub = [[0,0],[0,1],[0,2],[0,3],[1,0],[1,1],[1,2],[1,3],[2,0],[2,1],[2,2],[2,3],[3,0],[3,1],[3,2],[3,3]]
        index = 0
        for t in templatesList:
            lx=[]
            ly=[]
            if isProtractor==False:
                for x,y in t[1]:
                    lx.append(x)
                    ly.append(y)
                if index == template_final_index:
                    axs[sub[i][0],sub[i][1]].set_facecolor('#C4FFC9')

                axs[sub[i][0],sub[i][1]].set_title(t[0].capitalize())
                axs[sub[i][0],sub[i][1]].scatter(lx, ly, s =[6],c='red')
                axs[sub[i][0],sub[i][1]].plot(lx,ly, 'r:')
                axs[sub[i][0],sub[i][1]].scatter(fx, fy, s =[6],c='blue')
                axs[sub[i][0],sub[i][1]].plot(fx,fy, 'b:')
                axs[sub[i][0],sub[i][1]].invert_yaxis()


            else:
                for j in range(0, len(t[2])-1, 2):
                    lx.append(t[2][j])
                    ly.append(t[2][j+1])
                if index == template_finalP_index:
                    axs[sub[i][0],sub[i][1]].set_facecolor('#C4FFC9')
                axs[sub[i][0],sub[i][1]].set_title(t[0].capitalize())
                axs[sub[i][0],sub[i][1]].scatter(lx, ly, s =[10],c='red')
                axs[sub[i][0],sub[i][1]].plot(lx,ly, 'r:')
                axs[sub[i][0],sub[i][1]].scatter(fx, fy, s =[10],c='blue')
                axs[sub[i][0],sub[i][1]].plot(fx,fy, 'b:')
                axs[sub[i][0],sub[i][1]].invert_yaxis()

            i+=1
            index+=1
        plt.show()
##############################################################################################################################################################################################
###
