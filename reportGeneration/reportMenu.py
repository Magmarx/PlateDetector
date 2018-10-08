#Author Mporras
#Date 13/sep/2018
''' 
This is the file that will manage all the variations on the report generating methods
'''

import sys
from reportGenerator import readFolder, readFile, readFolder_Car_NoCar


# python reportGenerator.py --folder --reportType  --dev/prod path 

# Arg 1 is the reading data because you can generate a report from a file or a folder (--folder/--file)
executionMethod = ''
# Arg 2 is the flag that will tell the report type to generate (--Early_Morning/--Morning/--Afternoon/--Night/--General)
reportType = ''
# Arg 3 is the dev/prod flag to know what type of report we will produce
isDev = '--prod'
# Arg 4 is the path of the data we will create a report of
path = ''
# flag that will activate just if its the general report
generalReport = False

if len(sys.argv) > 1:
    executionMethod = sys.argv[1]
if len(sys.argv) > 2:
    reportType = sys.argv[2]
if len(sys.argv) > 3:    
    isDev = sys.argv[3]
if len(sys.argv) > 4:
    path = sys.argv[4]

if reportType == "--Early_Morning":
    path += "/Early_Morning/"
elif reportType == "--Morning":
    path += "/Morning/"
elif reportType == "--Afternoon" :
    path += "/Afternoon/"
elif reportType == "--Night":
    path += "/Night/"
else:
    print("Pending for dev...")
    # generalReport = True
    

if not generalReport:
    if executionMethod == "--folder":
        devFlag = True if isDev == "--dev" else False
        if devFlag:
            readFolder_Car_NoCar(executionMethod, reportType, isDev, path)
            readFolder(executionMethod, reportType, isDev, path)
        else:
            readFolder(executionMethod, reportType, isDev, path)
    elif executionMethod == "--file":    
        readFile(executionMethod, reportType, isDev, path)    
    else: 
        print("Invalid arg")
else:
    paths = [path + "/Early_Morning/car/", path + "/Morning/car/", path + "/Afternoon/car/", path + "/Night/car/"]
    readMultiplePaths(paths, isDev)