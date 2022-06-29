try:
    import sys
    import os
    import csv
    import ntpath
    import shutil
    import subprocess
    import xlsxwriter 


    import cv2
    import matplotlib.pyplot as plt
    from deepface.extendedmodels import Age, Gender, Race, Emotion
    from deepface import DeepFace
    from moviepy.editor import VideoFileClip
    from tkinter import filedialog
    from tkinter import *
    from tkinter import Tk
    from tkinter.filedialog import askdirectory

except Exception as e:
    print('Some Modules are missing {}'.format(e))


# A method to find most frequent element in a list
def most_frequent(List):
    counter = 0
    num = List[0]

    for i in List:
        curr_frequency = List.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            num = i

    return num

# A method for getting the filename from filepath
def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

# A method for getting the duration of the video
def get_length(filename):
    clip = VideoFileClip(filename)
    return clip.duration

# Main method
def main():

	filenames = []

	# Ask the user for a directory path
	directoryPath = askdirectory(title='Select folder to perform emotion detection:')
	directory = os.fsencode(directoryPath)

	# Traverse each file in the directory and save the paths in the filenames variable
	for file in os.listdir(directory):
		filename = directoryPath+'/'+os.fsdecode(file)
		filenames.append(filename)

	print('-> This may take a while...')

	# A boolean that decides whether a detector backend should be used in the prediction model
	# By default I have defined it as False
	# However, by changing it you may get some better results
	detectorBackend = False

	# Threshold value for keeping a prediction by the model
	# By default I have defined it as 0
	# However, by changing it you may get some better results
	thresholdValueForPrediction = 0

	# Perform the prediction for each file in the directory
	for filename in filenames:
	    
	    # Video file name (must be in same folder)
	    videoName = filename

	    # Get the video`s duration
	    # (We use it in order to calculate the fps block value)
	    videoDuration = get_length(videoName)
	    print('-- Video duration: '+str(videoDuration)+' seconds')

	    # For pathname extraction
	    ntpath.basename("a/b/c")

	    # The filename 
	    # (We will use it to name our reports)
	    outputName = path_leaf(videoName)

	    # Remove the file extension from the name
	    outputName = outputName.split('.', 1)[0]

	    # Create the folder where we will save our output
	    folderName = outputName + '_results'

	    # Create the results folder
	    try:
	        os.mkdir(folderName)
	    except OSError:
	        print("ERROR - Creation of the directory %s failed" % folderName)
	    else:
	        print("ERROR - Successfully created the directory %s " % folderName)

	    # We want to disable the prints
	    # This is done because deepface prints a lot of lines during the process. This is an easy workaround to avoid the spam :)
	    blockPrint()

	    # Loading pre-trained models
	    # In the first run of the program, this will download the models to your drive (expect 2 - 3 GB of space being occupied)
	    models = {}
	    models["emotion"] = Emotion.loadModel()
	    models["age"] = Age.loadModel()
	    models["gender"] = Gender.loadModel()
	    models["race"] = Race.loadModel()

	    # init HASHMAP with emotion values
	    emotionsMap = {}
	    emotionsMap['angry'] = 0
	    emotionsMap['disgust'] = 0
	    emotionsMap['fear'] = 0
	    emotionsMap['happy'] = 0
	    emotionsMap['sad'] = 0
	    emotionsMap['surprise'] = 0
	    emotionsMap['neutral'] = 0

	    # List containing all the possible emotions
	    allEmotionsList = []
	    # emotion color representation
	    allEmotionsColors = ['r', 'y', 'darkgray', 'g', 'b', 'm', 'c']
	    # emotions values
	    allEmotionsValues = []
	    # List containing the prediction values. This will be used in order to create the plot
	    emotionsResultList = []
	    # List containing the estimated accuracy value of a certain prediction
	    predictionAccuracyList = []
	    # This list will be used to highlight the dominant emotion in the video
	    explodeValues = []

	    # A map cotaining the accuracy of emotion predictions for each frame
	    frameEmotionsMap = {}

	    # init emotions map
	    tmpEmotionsList = []
	    for emotion in emotionsMap:
	    	tmpEmotionsList.append(emotion)

	    # first line contains the emotions in order
	    frameEmotionsMap[0] = tmpEmotionsList

	    # Frames
	    framesList = []

	    # read video
	    vidcap = cv2.VideoCapture(videoName)
	    success, image = vidcap.read()
	    count = 0

	    # begin
	    while success:
	        # read frame
	        success, image = vidcap.read()

	        if success == False:
	            break
	        if success:
	            # analyze frame using pre-trained models
	            if detectorBackend:
	            	result = DeepFace.analyze(image, models=models, actions=['emotion'], enforce_detection=False, detector_backend=detectorBackendValue)
	            else:
	            	result = DeepFace.analyze(image, models=models, actions=['emotion'], enforce_detection=False)

	            # Total emotions list for the frame
	            frameEmotions = []

	            # If the result is higher that the selected threshold, we keep it
	            if result['emotion'][result['dominant_emotion']] >= thresholdValueForPrediction:
	                emotionsMap[result['dominant_emotion']] += 1
	                emotionsResultList.append(result['dominant_emotion'])
	                predictionAccuracyList.append(result['emotion'][result['dominant_emotion']])
	            else:
	                emotionsMap['undefined'] += 1
	                emotionsResultList.append('undefined')
	                predictionAccuracyList.append(result['emotion'][result['dominant_emotion']])

	            # For each emotion save the prediction accuracy value in the frameEmotions List
	            for emotion in emotionsMap:
	            	frameEmotions.append(result['emotion'][emotion])

	           	# append the list of emotion accuracy 
	            frameEmotionsMap[count+1] = frameEmotions

	        count += 1;
	        framesList.append(count)

	    # re-enable the prints
	    enablePrint()

	    # When everything done, release the capture
	    vidcap.release()
	    cv2.destroyAllWindows()

	    # init some useful variables for generating the output
	    emotionsCount = 0
	    emotionPercentages = {}
	    dominantOverallEmotion = 'unknown'
	    dominantOverallEmotionValue = -1

	    if count > 0:
	        # Open output file to write to...
	        textFile = open(outputName+'-results.txt', "w")

	        textFile.write('Results for video: ' + outputName + '\n\n')

	        print('Occurances of each emotion in used frames: ')
	        textFile.write('Occurances of each emotion in used frames: \n')

	        for emotion in emotionsMap:
	            print(emotion + ' : ' + str(emotionsMap[emotion]))
	            textFile.write(emotion + ' : ' + str(emotionsMap[emotion]) + '\n')
	            emotionsCount = emotionsCount + emotionsMap[emotion]

	        print(str(emotionsCount) + ' frames out of : ' + str(count) + ' were used...')
	        textFile.write(str(emotionsCount) + ' frames out of : ' + str(count) + ' were used...\n')

	        print('Percentages of each emotion in frames used: ')
	        for emotion in emotionsMap:
	            print(emotion + ' : ' + str((emotionsMap[emotion]/emotionsCount)*100) + '%')
	            textFile.write(emotion + ' : ' + str((emotionsMap[emotion]/emotionsCount)*100) + '%\n')
	            allEmotionsList.append(emotion)
	            allEmotionsValues.append((emotionsMap[emotion]/emotionsCount)*100)
	            emotionPercentages[emotion] = (emotionsMap[emotion]/emotionsCount)*100

	        print('--> Dominant emotion in video: ')
	        textFile.write('--> Dominant emotion in video: \n')
	        for emotion in emotionsMap:
	            if emotionPercentages[emotion] > dominantOverallEmotionValue:
	                dominantOverallEmotion = emotion
	                dominantOverallEmotionValue = emotionPercentages[emotion]
	        print(dominantOverallEmotion + ' : ' + str(dominantOverallEmotionValue) + '%')
	        textFile.write(dominantOverallEmotion + ' : ' + str(dominantOverallEmotionValue) + '%\n')

	        textFile.write('\n')
	        textFile.write('FPS: '+str(int(emotionsCount / videoDuration))+'\n')
	        textFile.write('Duration: ' + str(videoDuration) + ' seconds'+'\n')

	        # Closing the output file...
	        textFile.close()

	        # move txt to output folder
	        shutil.move(outputName + "-results.txt", folderName)

	       
	        ## Creating the csv output Frame - Emotions Prediction Accuracy
	        csvPerFrameEmotionAccuracyName = outputName + '-emotion-detection-results-per-frame-total-accuracy.csv'
	        with open(csvPerFrameEmotionAccuracyName,mode='w') as resultsCSV:
	            resultsCSV = csv.writer(resultsCSV, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

	            # creating the first row
	            tmpFirstRowList = []
	            tmpFirstRowList.append('Frame')
	            for emotion in frameEmotionsMap[0]:
	            	tmpFirstRowList.append(emotion)
	            resultsCSV.writerow(tmpFirstRowList)

	            # for each frame we get the list containing the respective accuracy prediction values...
	            for row in range(len(framesList)):
	            	tmpRowList = []
	            	tmpRowList.append(row+1)
	            	for value in frameEmotionsMap[row+1]:
	            		tmpRowList.append(value)

	            	resultsCSV.writerow(tmpRowList)

	        # move csv to output folder
	        shutil.move(csvPerFrameEmotionAccuracyName, folderName)

	        ## Creating the xlsx containing the output Frame - Emotions Prediction Accuracy
	        xlsxPerFrameEmotionAccuracyName = outputName + '-emotion-detection-results-per-frame-total-accuracy.xlsx'
	        workbook = xlsxwriter.Workbook(xlsxPerFrameEmotionAccuracyName)
	        worksheet = workbook.add_worksheet(xlsxPerFrameEmotionAccuracyName.split('.', 1)[0][0:31])
	        worksheet.write(0,0,'Frame')
	        for i in range(len(frameEmotionsMap[0])):
	        	worksheet.write(0,i+1,frameEmotionsMap[0][i])

	       	# for each frame we get the list containing the respective accuracy prediction values...
	        row = 1
	        for i in range(len(framesList)):
	        	worksheet.write(row,0,i+1)
	        	j = 1
	        	for value in frameEmotionsMap[i+1]:
	        		worksheet.write(row,j,value)
	        		j += 1
	        	row += 2
	        workbook.close()

	        # move xlsx to output folder
	        shutil.move(xlsxPerFrameEmotionAccuracyName, folderName)

	        # -- End of main()

# Disable Prints
def blockPrint():
    sys.stdout = open(os.devnull, 'w')

# Restore Prints
def enablePrint():
    sys.stdout = sys.__stdout__

#----------------------------------------------------- Program Code here -----------------------------------------------------

print('----------------------------------------------------- Welcome to emotion detection with deepface -----------------------------------------------------')
main()
print('-> Bye bye!')
sys.exit('main exit');
