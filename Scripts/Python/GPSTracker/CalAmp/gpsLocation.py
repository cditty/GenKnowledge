#!/usr/bin/python
import socket
import string
import time
import requests
import config
import subprocess

while True:
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((config.UDP_IP, config.UDP_PORT))
	
	data, addr = sock.recvfrom(4096)
	#print data
	
	gpsInfoNorth = data.split("+")
	gpsInfoWest = gpsInfoNorth[1].split("-")
	gpsInfoTruck = gpsInfoWest[1].split("=")
	gpsInfoTruck = gpsInfoTruck[1].split(";")

	gpsNorth = gpsInfoNorth[1][:2] + "." + gpsInfoNorth[1][2:7]
	gpsWest = "-" + gpsInfoWest[1][:3] + "." + gpsInfoWest[1][3:8]
	gpsTruck = gpsInfoTruck[0]

	print (gpsNorth + ", " + gpsWest + " - " + gpsTruck)
	print (config.urlServer + "?gpsN=" + gpsNorth + "&gpsW=" + gpsWest + "&truckNbr=" + gpsTruck)

	# Time to pass the GPS info to the internal server
	r = requests.get(config.urlServer + "?gpsN=" + gpsNorth + "&gpsW=" + gpsWest + "&truckNbr=" + gpsTruck)
	#print (r.status_code)
	#print (r.headers)
	#print (r.content)

	clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	clientsocket.connect(('localhost', 5830))
	clientsocket.send("gpsN=" + gpsNorth + "&gpsW=" + gpsWest + "&truckNbr=" + gpsTruck)

	# Sleep for 5 seconds
	time.sleep(5)
else:
	rebootCommand = "sudo /home/pi/Documents/scripts/reboot.sh"
	output = subprocess.check_output(['bash','-c', rebootCommand])
	
sock.close()
