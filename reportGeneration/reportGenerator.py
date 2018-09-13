#Author Mporras
#Date 13/sep/2018
# import sys 
from os import listdir
from os.path import isfile, join
import ast
from openpyxl import Workbook

def readFolder(executionMethod, reportType, isDev, path):

    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    filePlates = []
    cars = []
    for fileName in onlyfiles:
        # print("Generating " + fileName)
        readFileResult = readFile(executionMethod, reportType, isDev, path + fileName)
        # print(readFileResult)
        if readFileResult != None:
            cars.append(readFileResult[0])
            filePlates.append(readFileResult[1])        
        # results.append(filePlates)    
    # return results
    # print(filePlates)
    if reportType == "--Early_Morning":
        generateEarlyMorningReport(cars, filePlates)
    elif reportType == "--Morning":
        generateMorningReport(cars, filePlates)
    elif reportType == "--Afternoon" :
        generateAfternoonReport(cars, filePlates)
    elif reportType == "--Night":
        generateNightReport(cars, filePlates)
    else:
        ### pending for development
        generateGeneralReport(cars, filePlates)

    pass

def readFile(executionMethod, reportType, isDev, path):
    i = 0
    devFlag = True if isDev == "--dev" else False
    cars = []
    plates = []

    if path.find(".DS_Store") < 0:        
        file = open(path, 'r')
        for line in file:
            if devFlag and i < 3:
                cars.append(line)
            else:
                plates.append(line)
            i += 1  
        return (cars, plates)
          
    pass

def generateEarlyMorningReport(cars, plates):
    
    wb = Workbook()
    ws = wb.active

    titles = ["Video", "Placa", "Porcentaje", "Tipo de placa", "Correcta/Incorrecta", "Path"]
    ws.append(titles)
    i = 0

    for value in plates:            
        if len(value) == 0:       
            print("File not found")                       
            ws.append([cars[i][2] + ".mp4", '', '', '', '', cars[i][1].replace("\n", ".mp4")])

        for plate in value:
            plate = plate.split(",")
            plate[len(plate) - 1] = plate[len(plate) - 1].split(".mp4")[0] + ".mp4"
            ws.append(plate)

        i += 1

    wb.save("./reportGeneration/reports/Early_Morning/Early_Morning.xlsx")        
    
    pass

def generateMorningReport(cars, plates):    
    wb = Workbook()
    ws = wb.active

    titles = ["Video", "Placa", "Porcentaje", "Tipo de placa", "Correcta/Incorrecta", "Path"]
    ws.append(titles)
    i = 0

    for value in plates:            
        if len(value) == 0:       
            print("File not found")                       
            ws.append([cars[i][2] + ".mp4", '', '', '', '', cars[i][1].replace("\n", ".mp4")])

        for plate in value:
            plate = plate.split(",")
            plate[len(plate) - 1] = plate[len(plate) - 1].split(".mp4")[0] + ".mp4"
            ws.append(plate)

        i += 1

    wb.save("./reportGeneration/reports/Morning/Morning.xlsx")        
    pass

def generateAfternoonReport(cars, plates):
    wb = Workbook()
    ws = wb.active

    titles = ["Video", "Placa", "Porcentaje", "Tipo de placa", "Correcta/Incorrecta", "Path"]
    ws.append(titles)
    i = 0

    for value in plates:            
        if len(value) == 0:       
            print("File not found")                       
            ws.append([cars[i][2] + ".mp4", '', '', '', '', cars[i][1].replace("\n", ".mp4")])

        for plate in value:
            plate = plate.split(",")
            plate[len(plate) - 1] = plate[len(plate) - 1].split(".mp4")[0] + ".mp4"
            ws.append(plate)

        i += 1

    wb.save("./reportGeneration/reports/Afternoon/Afternoon.xlsx")        
    pass

def generateNightReport(cars, plates):
    wb = Workbook()
    ws = wb.active

    titles = ["Video", "Placa", "Porcentaje", "Tipo de placa", "Correcta/Incorrecta", "Path"]
    ws.append(titles)
    i = 0

    for value in plates:            
        if len(value) == 0:       
            print("File not found")                       
            ws.append([cars[i][2] + ".mp4", '', '', '', '', cars[i][1].replace("\n", ".mp4")])

        for plate in value:
            plate = plate.split(",")
            plate[len(plate) - 1] = plate[len(plate) - 1].split(".mp4")[0] + ".mp4"
            ws.append(plate)

        i += 1

    wb.save("./reportGeneration/reports/Night/Night.xlsx")        

    pass

### pending for development
def generateGeneralReport(cars, plates):
    pass