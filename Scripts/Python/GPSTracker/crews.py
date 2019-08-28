import serial
import time
import os
import subprocess
import requests
import urllib3
import re

##########################
# User Definable Section #
##########################
# Time between updates
updateTime = 15

# Server address to hit to process GPS data
urlServer = 'https://'

# Debug mode?
debug = False
debugSleep = 0

##########################
# Don't touch after this #
##########################
# Disable SSL Serurity Warnings
urllib3.disable_warnings()

# Do we have a valid WiFi Signal
wifiStr = False

# What is my user ID
myUserID = os.getenv('username').lower()
if myUserID == 'cf31gridpad2':
     myUserID = 'admin'
elif myUserID == 'cditt':
    myUserID = 'admin'

#############
# Functions #
#############
# Used to convert GPS from degrees to decimal
def gpsConvert(degrees, minutes):
    converted = int(degrees) + float(minutes)/60
    return converted

# this searches the gpsVar for alpha chars
def gpsCheck(gpsVar):
    return re.search('[a-zA-Z]', gpsVar)

# This will check to make sure there is only 1 . in the gps string
def gpsCheck2(gpsVar):
    if gpsVar.count('.') == 1:
        return True
    else:
        return False

def getMachineName():
    return os.environ['COMPUTERNAME']

def submitWebResults(urlServer, gpsN, gpsW, crewID, wifiStr, updateTime,  debug):
    try:
        if debug:
            print("Command sent: " + urlServer + "?gpsN=" + gpsNorth + "&gpsW=-" + gpsWest + "&crewID=" + myUserID + "&cellStr=-" + wifiStr + "&padName=" + getMachineName())
            time.sleep(debugSleep)

        r = requests.get(urlServer + "?gpsN=" + gpsNorth + "&gpsW=-" + gpsWest + "&crewID=" + myUserID + "&cellStr=-" + wifiStr + "&padName=" + getMachineName(), verify=False)
        #print(str(r.status_code))

        # Sleep 
        time.sleep(updateTime)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
        print (e)
        time.sleep(120)

    return False

def getWifiStr(gridpadModel, debug):
    wifiStr = False
    if GRIDPAD_MODEL == "CF-31-2": # Older gridpads
            # Let's find out the wifi signal strength
            GetWifiInfo = "C:\\progra~1\\python36\\misc\\snmpget -v:2c -c:public -r:10.166.0.1 -p:161 -o:.1.3.6.1.4.1.3732.7.3.3.4.1.6.0"
            myWifiStr = subprocess.Popen(GetWifiInfo,
                        stdout=subprocess.PIPE,
                        shell=True)
            
            for line in iter(myWifiStr.stdout.readline, b''):
                myLine = line.decode('utf-8', "replace").rstrip().lstrip()
                if(myLine[0:6] == "Value="):
                    WifiStr = myLine.split("dBm")
                    WifiStr = WifiStr[0].split("=")
                    wifiStr = WifiStr[1][1::]
                    
                    if debug:
                        print("Wifi Str: " + wifiStr)
                        time.sleep(debugSleep)
                    
    else: # Newer gridpads
        # Use the MS netsh command to get the cell strength
        # This must be run in 64 bit mode or it won't work
        p = subprocess.Popen('netsh mbn show interfaces', 
                    stdout = subprocess.PIPE,
                    stderr = subprocess.PIPE,
                    shell = True)

        for line in iter(p.stdout.readline, b''):
            if len(line) > 4:
                myLine = line.decode('utf-8', "replace").rstrip().lstrip()

                if myLine[0:6] == "Signal":
                    # Split on the ": "
                    myWifilStr = myLine.split(": ")
                    
                    # Reverse to strip % symbol
                    wifiStr = myWifilStr[1][::-1]

                    # Strip % symbol and reverse again
                    wifiStr = wifiStr[1:3][::-1]

                    if debug:
                        print("Wifi Str: " + wifiStr)
    if wifiStr == "/A":
        return False
    else:
        return wifiStr

# Get the Machine Model
sysInfo = subprocess.Popen('systeminfo',
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True)

for infoLine in iter(sysInfo.stdout.readline, b''):
    myInfoLine = infoLine.decode('utf-8', "replace").rstrip().lstrip()
    if debug:
        print(myInfoLine)
        time.sleep(debugSleep)

    if myInfoLine[0:13] == "System Model:":
        # Need to split on the ": "
        mySysInfo = myInfoLine[27:35]

        # We have the machine model now
        if mySysInfo == "CF-33-1":
            # This is the com port that the GPS chip communicates on
            SERIAL_PORT = 'COM6'

            # This is the baud rate for the gps
            SERIAL_RATE = 9600

            # This tells us the model
            GRIDPAD_MODEL = "CF-33-1"
        elif mySysInfo == "CF-31-5" or mySysInfo == "CF-31-6":
            # This is the com port that the GPS chip communicates on
            SERIAL_PORT = 'COM3'

            # This is the baud rate for the gps
            SERIAL_RATE = 9600

            # This tells us the model
            GRIDPAD_MODEL = "CF-31-5"
        else:
             # This is the com port that the GPS chip communicates on
            SERIAL_PORT = 'COM3'

            # This is the baud rate for the gps
            SERIAL_RATE = 4800

            # This tells us the model
            GRIDPAD_MODEL = "CF-31-2"

if debug:
    print("Com Port: " + SERIAL_PORT)
    time.sleep(debugSleep)

# The guts of the program
ser = serial.Serial(SERIAL_PORT, SERIAL_RATE)
while True:
    wifiStr = False
    gpsNorth = False
    gpsWest = False

    # We have a user id?
    if debug:
        print("User ID: " + myUserID)
        time.sleep(debugSleep)

    # Need to take the string being fed and decode it
    reading = ser.readline().decode('UTF-8', "replace")
    
    if debug:
        print(reading[0:6] + " - " + reading)
        time.sleep(debugSleep)

    # This is the string we are looking for
    #$GNGLL,194254.00,3510.27155,N,08950.22412
    # Depending on the model, we are looking for $GNGGA or GPGGA
    if GRIDPAD_MODEL == "CF-31-2":
        GPS_SearchTerm = "$GPGGA"
    elif GRIDPAD_MODEL == "CF-33-1":
        GPS_SearchTerm = "$GPGLL"
    else:
        GPS_SearchTerm = "$GNGLL"

    if reading[0:6] == GPS_SearchTerm:
        gpsReading = reading.split(",")

        # this is to handle when the GPS chip doesn't return a valid string
        # GPS North
        try:
            if isinstance(gpsReading[1], str):
                gpsReadingNorth = gpsReading[1]
            else:
                gpsReadingNorth = False
        except IndexError:
            gpsReadingNorth = False

        try:
            if isinstance(gpsReading[1], str):
                gpsReadingWest = gpsReading[3]
            else:
                gpsReadingWest = False
        except IndexError:
            gpsReadingWest = False

        #if debug:
            #print(gpsReadingNorth + " -- " + gpsReadingWest)
            #time.sleep(debugSleep)
        
        # Do we have a valid gps?
        if gpsReadingNorth != False and gpsReadingWest != False:
            # The gps chip sometimes dumps extra data.  Limiting to under 90 chars for consistancy
            if len(gpsReadingNorth) == 10 and len(gpsReadingWest) == 11 and len(reading) < 90 and not gpsCheck(gpsReadingNorth) and not gpsCheck(gpsReadingWest) and gpsCheck2(gpsReadingWest) == True:
                if debug:
                    print("GPS North - " + gpsReadingNorth[:2] + " -- " +  gpsReadingNorth[2:])
                    print("GPS West - " + gpsReadingWest[:3] + " -- " +  gpsReadingWest[3:])
                    time.sleep(debugSleep)

                lat = gpsConvert(str(gpsReadingNorth[:2]), str(gpsReadingNorth[2:]))
                lon = gpsConvert(str(gpsReadingWest[:3]), str(gpsReadingWest[3:]))
                gpsNorth = str(lat)[:8]
                gpsWest = str(lon)[:8]

                # Get the wifi strength
                wifiStr = getWifiStr(GRIDPAD_MODEL, debug)

                if wifiStr:
                    if debug:
                        print("GPS North: " + gpsNorth)
                        print("GPS West: " + gpsWest)
                        print("User ID: " + myUserID)
                        print("Wifi Str: " + wifiStr)
                        time.sleep(debugSleep)

                    # Submit the results
                    submitWebResults(urlServer, gpsNorth, gpsWest, myUserID, wifiStr, updateTime, debug)
