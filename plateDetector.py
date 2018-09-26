#Author Mporras
#Date 13/sep/2018
import urllib.request as M5Request
import urllib.parse as M5Parser
import urllib
import time
import json
import subprocess
import subprocess
import os
import re
import arrow

from os import listdir
from os.path import isfile, join
from utils import flatMap, reduceByKey
from collections import Counter
import shutil

'''
This method recieves the path of the folder where the files are and if it will use log
the log will enter with the value noLog if no log will be displayed or --log if a log 
will be displayed
'''
def readFolder(path, log, delete, jsonData, reportFlag, repDate, repTime, dev, channel):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    results = []
    for fileName in onlyfiles:
        print("Analyzing " + fileName)
        filePlates = readFile(path + fileName, log, delete, jsonData, reportFlag, repDate, repTime, dev, channel)
        if log == "--log":
            print(filePlates)
            print("\n")
        results.append(filePlates)
    print("analized files : " + str(len(onlyfiles))) 
    return results

'''
This method recieves the path of the file calls the functions to analyze the file and find
the plate
'''
def readFile(path, log, delete, jsonData, reportFlag, repDate, repTime, dev, channel):
    initialMillis = int(round(time.time() * 1000))    

        # This configuration will create a log with all the process of the plate detection
    if log == "--text":        
        splitPath = path.split("/")
        if len(splitPath) < 2:
            splitPath = path.split("\\")
        fileNameWithExtention = splitPath[len(splitPath) - 1]
        fileName = fileNameWithExtention.split(".")[0]
        file = open("./logFiles/" + "logFile" + arrow.now().format('YYYY-MM-DD') + "-" + fileName + ".txt","w") 
 
        # here we write the log of the raw plate detection 
        file.write(path + "\n")   
        file.write("plate log \n")
        plateLog = readVideo(path)
        file.write(plateLog + "\n")

        # here we write the log of the plates after we splitted them
        file.write("splited plates \n")
        splitedPlates = splitPlatesResults(plateLog)
        file.write(splitedPlates + "\n")        
        platesPairs = convertDataToPair(splitedPlates)            

        #here we write the plates after we made them on to consistant results
        file.write("Plates \n")
        licencePlates = compressPlates(platesPairs[0], platesPairs[1])
        licencePlates.sort(key=sortSecond, reverse=True)            
        file.write(str(licencePlates).strip('[]'))
        endMillis = int(round(time.time() * 1000))    
        procesTimeMillis = endMillis - initialMillis
        file.write("\n")

        # we write the process time 
        file.write("Final time \n")
        file.write(str(procesTimeMillis) + " ms")
        file.write("\n")
        file.write(str(procesTimeMillis / 1000) + " s")
        file.close() 
        # here we create the report file to leave for further analysis
        createReportFile(splitedPlates, platesPairs, licencePlates, path, reportFlag, repDate, repTime, dev, jsonData, channel)

        # this configuration will call a rest to create a transaction and send it to M5
    elif log == "--rest":         
        plateLog = readVideo(path)
        splitedPlates = splitPlatesResults(plateLog)
        platesPairs = convertDataToPair(splitedPlates)    
        licencePlates = compressPlates(platesPairs[0], platesPairs[1])
        licencePlates.sort(key=sortSecond, reverse=True)    
        if len(licencePlates) > 0 :
            callRest(licencePlates[:3], jsonData, path)    
        # here we create the report file to leave for further analysis
        createReportFile(splitedPlates, platesPairs, licencePlates, path, reportFlag, repDate, repTime, dev, jsonData, channel)
    else:
        plateLog = readVideo(path)
        splitedPlates = splitPlatesResults(plateLog)
        platesPairs = convertDataToPair(splitedPlates)    
        licencePlates = compressPlates(platesPairs[0], platesPairs[1])
        licencePlates.sort(key=sortSecond, reverse=True)    
        # here we create the report file to leave for further analysis
        createReportFile(splitedPlates, platesPairs, licencePlates, path, reportFlag, repDate, repTime, dev, jsonData, channel)
        endMillis = int(round(time.time() * 1000))    
        procesTimeMillis = endMillis - initialMillis
        print("Final time")
        print(str(procesTimeMillis) + " ms")
        print(str(procesTimeMillis / 1000) + " s")
        print(licencePlates)  
    
    # if this flag is active the video will be deleted
    if delete == '--del':
        os.remove(path)
        
    return licencePlates


'''
This method will write the file report for analysis
'''
def createReportFile(splitedPlates, platesPair, licencePlates, path, report, date, time, dev, params, channel):    
    
    splitPath = path.split("/")
    if len(splitPath) < 2:
        splitPath = path.split("\\")
    fileNameWithExtention = splitPath[len(splitPath) - 1]
    fileName = fileNameWithExtention.split(".")[0]
    dirName = ''
    dirNameFile = ''
    data = ''    

    if report == '--report':    
        isCar = checkCar(platesPair)     
        date = date.split("/")
        year = date[2]       
        month = date[1]
        day = date[0]
        if not(isCar) and (dev == "--dev"):
            intTime = int(time)            
            if intTime < 5 and intTime > 0:
                dirName = "./" + params[8] + "/" + channel + "/" + year + "/" + month + "/" + day + "/" + "Early_Morning/notCar/"                
                data += 'Not car\n' + dirName + fileName + "\n" + fileName                
            if intTime < 12 and intTime > 5:
                dirName = "./" + params[8] + "/" + channel + "/" + year + "/" + month + "/" + day + "/" + "Morning/notCar/"
                data += 'Not car\n' + dirName + fileName + "\n" + fileName
            if intTime < 18 and intTime > 12:
                dirName = "./" + params[8] + "/" + channel + "/" + year + "/" + month + "/" + day + "/" + "Afternoon/notCar/"
                data += 'Not car\n' + dirName + fileName + "\n" + fileName
            if intTime <= 23 and intTime > 18:
                dirName = "./" + params[8] + "/" + channel + "/" + year + "/" + month + "/" + day + "/" + "Night/notCar/"
                data += 'Not car\n' + dirName + fileName + "\n" + fileName

        elif isCar:
            intTime = int(time)  
            print(licencePlates)          
            if intTime <= 5 and intTime > 0:
                dirName = "./" + params[8] + "/" + channel + "/" + year + "/" + month + "/" + day + "/" + "Early_Morning/car/"
                data += 'Car\n' + dirName + fileName + "\n" + fileName + "\n"                
            if intTime <= 12 and intTime > 5:
                dirName = "./" + params[8] + "/" + channel + "/" + year + "/" + month + "/" + day + "/" + "Morning/car/"
                data += 'Car\n' + dirName + fileName + "\n" + fileName + "\n"
            if intTime <= 18 and intTime > 12:
                dirName = "./" + params[8] + "/" + channel + "/" + year + "/" + month + "/" + day + "/" + "Afternoon/car/"
                data += 'Car\n' + dirName + fileName + "\n" + fileName + "\n"
            if intTime <= 23 and intTime > 18:
                dirName = "./" + params[8] + "/" + channel + "/" + year + "/" + month + "/" + day + "/" + "Night/car/"
                data += 'Car\n' + dirName + fileName + "\n" + fileName + "\n"
            i = 0
            for plate in licencePlates:                
                if i == 0:
                    data += fileName + " , " + plate[0] + " , " + str(plate[1]) + " , " + plate[2] +  " , Correct" + " , " + path + "\n"
                else:
                    data += fileName + " , " + plate[0] + " , " + str(plate[1]) + " , " + plate[2] +  " , Incorrect" + " , " + path + "\n"
                i += 1                                
                            
        if not os.path.exists(dirName): 
            os.makedirs(dirName)
            print("Directory " , dirName ,  " Created ")
        else:    
            print("Directory " , dirName ,  " already exists")  

        try:    
            file = open(dirName + fileName + ".txt" ,"w") 
            file.write(data)
            file.close()

        except ValueError:
            print("No logramos escribir el log")   

        try:    
            if dirName.find("notCar") > 0:
                newDir = dirName.replace('notCar/', 'video/notCar/')                

                if not os.path.exists(newDir): 
                    os.makedirs(newDir)
                    print("Directory " , newDir ,  " Created ")
                else:    
                    print("Directory " , newDir ,  " already exists")  

                shutil.move(path, newDir + fileName + ".mp4")
            else: 
                newDir = dirName.replace('car/', 'video/car/')

                if not os.path.exists(newDir): 
                    os.makedirs(newDir)
                    print("Directory " , newDir ,  " Created ")
                else:    
                    print("Directory " , newDir ,  " already exists")  

                shutil.move(path, newDir + fileName + ".mp4")
            

        except ValueError:
            print("No logramos mover el video al path")        

    

    pass

def checkCar(plates):
    result = False
    isCar = re.compile(r"[A-Z]+|[0-9]+",re.I)
    for plate in plates:
        for x,y in plate:
            if x != 'Time' and x != 'INFO:0]':
                if isCar.search(x):
                    result = True        
    return result
    pass

'''
This method will execute the command to analyze the images
'''
def readVideo(path):    
    return subprocess.run(['alpr', '--motion', '--clock', path], stdout=subprocess.PIPE).stdout.decode('utf-8')

'''
This method returns the percentaje of the plate when sorted
'''
def sortSecond(val):    
    return float(val[1])

'''
This method will split the string with the results of the plates, this will be splited by the 
word plate to find all the results
'''
def splitPlatesResults(plateLog):
    splitByPlate = plateLog.split('plate')
    sentence = ""

    for x in splitByPlate:    
        splitData = x.split('\n')
        startIndex = 1 
        if len(splitData) > 10:
            for y in splitData:

                if startIndex > 1 and startIndex <= 4:
                    finalSplit = y.split()
                    if len(finalSplit) > 3:
                        sentence += finalSplit[1] + "," + finalSplit[3] + " "

                startIndex += 1

    return sentence 

'''
This method will split data of the plate by a comma and will create a pair with 
the plate and the percentaje of accuracy.
'''
def convertDataToPair(splitedPlates):
    plateValues = []
    wordcount = []
    splitedSentence = splitedPlates.split()   

    for word in splitedSentence:        
        try:    
            plateData = word.split(',') 
            wordcount.append((plateData[0], 1))    
            plateValues.append((plateData[0],float(plateData[1])))

        except ValueError:
            print("No logramos convertir el dato")
    
    return (wordcount,plateValues)

'''
This method will allow us to filter the plates in a way where will will recieve 
only the plates that are certainly correct and will probably be the car plate
'''
def compressPlates(wordcount, plateValues):
    # we will merge all the plates into one
    resultWordCount = reduceByKey(lambda wordcount, b: b + b, wordcount)
    # we will create a sum with the percentages of the encountered plates
    resultPlateValues = reduceByKey(lambda plateValues, b: b + b, plateValues)
    higherValue = 0

    # here we will order the plates from higher to lower
    for w, z in resultWordCount:    
        if z > higherValue:
            higherValue = z
    
    lastWords = []
    # This regex will match only the coincidences like P987JIL
    license_plate = re.compile(r"^[A-Z][0-9]{3}[A-Z]{3}$",re.I)
    # This regex will match only the coincidences like 987JIL but 
    # this ones will have to be auto completed later
    license_plate_no_letter = re.compile(r"^[0-9]{3}[A-Z]{3}$",re.I)
    returnValues = []

    # Here we will se if the plate is a valid plate, or is a partial plate 
    # if its a partial plate we will have to add the P later on
    for plate, coincidences in resultWordCount:
        ml = "No "                
        if license_plate.search(plate): 
                ml = "Yes"          
        elif license_plate_no_letter.search(plate):
                ml = "Pyes"
            
        if ml == "Yes":
            lastWords.append((plate, "plate"))
        elif ml == "Pyes":
            lastWords.append((plate, "partialPlate"))              
    
    # here we will get the combined values of the sum plates and will get an average
    # accuracy from the combined plates and if the plates are incomplete we will complete them 
    for plate, percentaje in resultPlateValues:        
        for coincidences, typePlate in lastWords:                        
            if plate == coincidences:
                if typePlate == "partialPlate":
                    returnValues.append(("P" + plate, percentaje / higherValue, typePlate))
                else: 
                    returnValues.append((plate, percentaje / higherValue, typePlate))

    return returnValues

# here we will call the rest to create a M5 transaction
def callRest(plates, params, path):  

    '''
    the params that we recive are splitted by a the character ByteF
    we will spect the token on the first position, then 
    the recordCode then the uuidNode, the uuidModule, 
    etc. the order is static
    the order of this json can change
    '''

    jsonData = {
        'uuidToken': params[0],
        'recordCode': params[1],
        'uuidNode': params[2],
        'uuidModule': params[3],
        'nickNode': params[4],
        'nickModule': params[5],
        'fields':
            [
                {
                    # date 
                    'key': 0,
                    'value': params[6]
                },
                {
                    # time 
                    'key': 1,
                    'value': params[7]
                },
                {
                    # code
                    'key': 2,
                    'value': params[8]
                },
                {
                    # video (json) 
                    'key': 3,
                    'value': params[9].replace('"', '\\"')
                },
                {
                    # ip 
                    'key': 4,
                    'value': params[10]
                },                
                # {
                #     # channel 
                #     'key': 4,
                #     'value': params[11]
                # },                
                {
                    # name 
                    'key': 5,
                    'value': params[11].replace("_", " ")
                },
                {
                    # description 
                    'key': 6,
                    'value': params[12].replace("_", " ")
                },
                {
                    # plate1
                    'key': 7,
                    'value':plates[0][0] if len(plates) >= 1 else ''
                },
                {
                    # plate2
                    'key': 8,
                    'value': plates[1][0] if len(plates) >= 2 else ''
                },
                {
                    # plate3 
                    'key': 9,
                    'value': plates[2][0] if len(plates) >= 3 else ''
                },
                {
                    # video path 
                    'key': 10,
                    'value': path.replace('"', '\\"')
                },
                # {
                #     # Config 
                #     'key': 9,
                #     'value': params[-1]
                # }
            ]
    }       

    url = 'http://192.168.245.254:50005/Socket.svc/push'
    data = json.dumps(jsonData)
    data = str(data)
    data = data.encode('utf-8')    
    req = M5Request.Request(url, data, {'Content-Type': 'application/json'})
    resp = M5Request.urlopen(req)
    for x in resp:
        print(x)
    resp.close()
    pass