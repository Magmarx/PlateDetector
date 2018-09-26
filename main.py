#Author Mporras
#Date 13/sep/2018
''' 
This file is in charge to manage all the file operations to call the respective process
'''

import sys
from plateDetector import readFolder, readFile
# import json

# Arg 1 is for the execution method --folder or --file
executionMethod = sys.argv[1]
# Arg 2 is for the path of the file or folder 
mypath = sys.argv[2]
# Arg 3 is a flag for writing log write --log or --text to create a new file with the log or --rest to send a rest
uselog = 'noLog'
# Arg 4 is a flag for deleting the file activate by sending --del
delete = 'noDel'
# Arg 5 jsonData || --report flag
jsonData = ''
# Arg 6 is a flag to see if you will generate a report structure 
reportFlag = ''
# Arg 7 date for report
repDate = ''
# Arg 8 time for report
repTime = ''
# Arg 9 --dev --prod for generating different reports
dev = '--dev'
# Arg 10 channel
channel = 0

# Example python main.py --file filepath --opcion --noDel jsonData --report date time

# please install pip install arrow
if len(sys.argv) > 3:
    uselog = sys.argv[3]
if len(sys.argv) > 4:
    delete = sys.argv[4]
if len(sys.argv) > 5:    
    jsonData = sys.argv[5].split('ByteF')
if len(sys.argv) > 6:
    reportFlag = sys.argv[6]
if len(sys.argv) > 7:
    repDate = sys.argv[7]
if len(sys.argv) > 8:
    repTime = sys.argv[8]
if len(sys.argv) > 9:
    dev = sys.argv[9]
if len(sys.argv) > 10:
    channel = sys.argv[10]

if executionMethod == "--folder":
    print(readFolder(mypath, uselog, delete, jsonData, reportFlag, repDate, repTime, dev, channel))
elif executionMethod == "--file":    
    readFile(mypath, uselog, delete, jsonData, reportFlag, repDate, repTime, dev, channel)    
else: 
    print("Invalid arg")