About the File system:

1. Figures folder has all the figures. It has the following sub-folders/images:
	
	- All Graphs: Has all the graphs of accuracies and recognition time.
	- Custom dataset: Has all the figures related to Custom Dataset. It contains comparisons between $1 and protractor with respect to gesture mismatches.
	- Unistroke dataset: Has all the figures related to Unistroke Dataset, similar to the Custom dataset above.
	- Visualization: Just a few sample images of visualization steps.
	- Heatmap Image for All Users generated using GHosT.

2. Logfiles has four different files from both $1 and protractor on Unistroke and Custom Datasets.

3. User Gesture Dataset has the collected user data.

4. "$1+Protractor.exe" is the application and needs the "Gestures" Folder to be in the same directory to run. You can directly run it from this file structure.

5. "HCIRA-Project2-Presentation.pptx" has the presentation. If the images look too small, just look at them in the "Figures" sub-folder. Also, not all the images managed to be fit into the presentation (due to space, slides, and time constraints), so they can be found under the "Figures" sub-folder.

5. Python files: Main.py, Steps.py, TemplatesData.py, Unistroke.py

To only see protractor parts, see 3a, 3d, 3e 3g, and 4f.


##############################################################################################################################################################################################

NOTE: 
	
	- THE REPORT WILL CONTAIN DETAILED INFORMATION ABOUT ALL THE INSIGHTS.

	- THE "USE PROTRACTOR CHECKBOX" IS FOR OFFLINE RECOGNITION ONLY. FOR LIVE RECOGNITION, THE PROGRAM PREDICTS THE GESTURE ACCORDING TO BOTH $1 AND PROTRACTOR ALGORITHMS BY DEFAULT AND DISPLAYS IT ON THE SCREEN.
	- NO MODIFICATIONS WERE MADE TO THE CUSTOM DATASET FROM THE PREVIOUS PROJECT. IT IS ONLY INCLUDED SO THAT THE PROGRAM WORKS CORRECTLY. IMPORT THE "XML" FOLDER FROM THE AUTHORS' WEBSITE TO CHECK OFFLINE RECOGNITION FUNCTIONALITY.
	
	- THERE ARE 4 LOG FILES: $1 ON UNISTROKE AND CUSTOM DATASETS, AND PROTRACTOR ON UNISTROKE AND CUSTOM DATASETS. THESE FILES HAVE SOME NEW COLUMNS LIKE RECOGNITION TIME, NUMBER OF POINTS, AND SPEED (TIME TAKEN TO DRAW THE GESTURE). ALTHOUGH RECOGNITION TIME IS USED, THERE WERE NO SIGNIFICANT INSIGHTS FROM THE NUMBER OF POINTS AND SPEED.


##############################################################################################################################################################################################
##############################################################################################################################################################################################
##############################################################################################################################################################################################


Description:

1. TemplatesData.py: 

	It has a class called "GestureTemplates (line 2)". It has all the templates data which is taken from the authors' java code on the website.

##############################################################################################################################################################################################


2. Unistroke.py: 

	It uses "TemplatesData.py" and "Steps.py". It has a class called "Unistroke (line 5)" and has two functions: GetTemplates (line 8) and GetTemplatesProtractor (line 32) for getting the processed templates for $1 and $1+Protractor recognizers respectively. Both of these functions call the GetTemplate function from "Steps.py".

##############################################################################################################################################################################################

3. Steps.py:

	It has a class called "Steps (line 19)". It has several functions that are needed to perform the steps of 41 and protractor. The following are the functions:

	a. GetTemplate (line 21) is a function that preprocesses the points for $1 or protractor depending on the flag "isProtractor". It also stores the points at each phase which can be used for the visualization process later.

	b. Centroid (line 111) is a helper function that calculates the centroid of the set of points.
	
	c. boundingBox (line 123) is also a helper function that returns the position and dimensions of the bounding box.

	d. Step 1 (used by both $1 and protractor): Resampling 

		It has two functions: Resample (line 140) which resamples the points to specified 'n' value. It uses a function pathLength (line 134) to calculate the length of the whole path/gesture.

	e. Step 2 (used by both $1 and protractor): Rotate to Zero

		It has two functions: rotateToZero (line 178) which uses centroid (from line 111) and rotateBy (line 165) to rotate the whole gesture based on the angle between centroid and the first point. 

	f. Step 3: 

		-$1 Recognizer:

			i. scaleToSquare (line 188) will scale the gesture (250x250). It uses the boundingBox (line 123) function. Used by $1 only.
			ii.  translateToOrigin (line 199) will translate/move the whole gesture to origin. It uses the centroid function (line 111).

		-Protractor:
			
			It uses a function called Vcctorize (line 247), to vectorize the resampled points. It uses the functions centroid (line 111) and translateToOrigin (line 199).

	g. Step 4:

		- $1 Recognizer:

			It has a function distanceAtBestAngle (line 227) which uses distanceAtAngle (line 222) to calculate the best distance. distanceAtAngle again uses a function called pathDistance (line 227) to calculate the distance.

		- Protractor:

			It uses a different function called OptimalCosineDistance (line 266) which returns the optimal cosine distance. It returns a value between 1 and pi, so normalization can be done, but not necessary as we only use this value in comparison with other optimal cosine distances.


	h. Recognize (line 279):

		It recognizes the gesture. It uses GetTemplate (line 21), OptimalCosineDistance (line 266), and distanceAtBestAngle (line 227). It recognizes the gesture based on the algorithm used.

	i. Show (line 330):

		It is used to visualize all the gestures at each phase. It has access to the points saved at each phase and it shows them using multiple subplots. It uses show_recognition (line 435).

	ii. show_recognition (line 435)

		Used to show plots on template matching with the candidate.

##############################################################################################################################################################################################


4. Main.py:

	It is responsible for handling the GUI, calling all the above functions, and also the offline recognition parts. It uses "Unistroke.py" and "Steps.py".

	a. Lines 27 to 90 is live recognition. It uses functions: clear (line 30), start (line 36), draw (line 46), and on_release (line 54).

	b. Lines 92 to 294 are responsible for offline recognition. Based on the algorithm and which dataset to use, it performs offline recognition. The functions are:
		
		- offline at line 271: It calls the xmlparser (line 276) which reads the XML files. It also calls the offlineRecognizer (line 288) which performs the action.

	c. offlineRecogntion repeats the process 100 times. It uses recognize function from Steps.py to recognize the gestures and then writes all the information into a log file in the current directory.

	d. Lines 296 to 299 are to create a custom user dataset. It has functions add (line 359), savePoints (line 312) and endscreen (line 299). 

		- add: adds the points to a temporary list.
		- savePoints: saves the points once the user is finished.
		- endscreen: to notify the user, that everything is done.

	e. Line 432 has implemented to use custom dataset for offline recognition. This function is LoadCustomDataset.

	f. The rest of the code is to handle the GUI part of the code. So it doesn't need a description. But the code to enable or disable the protractor feature is implemented at line 594 using protractorEnable.



##############################################################################################################################################################################################
##############################################################################################################################################################################################
##############################################################################################################################################################################################