from phue import Bridge
import csv
import datetime
import sys
import serial
import time
import requests
import re
# Define Hue Bridge

b = Bridge('192.168.1.109')

#define tables
lStatus = []
lName = []
boxPos = ["2.2","7.2","12.2","2.7","7.7","12.7"]

s= serial.Serial()
s.baudrate = 9600
s.timeout = 0
s.port = "/dev/ttyAMA0"

try:
    s.open()
except serial.SerialException as e:
    sys.stderr.write("could not open port &r: %s\n" % (port, e))
    sys.exit(1)
def resetGrid():
	s.write(str.encode("$$$ALL,OFF\r"))

def drawGrid():
	# drawing horizontal lines
	for i in range(9):
		s.write(str.encode("$$$P5," + str(i+1) + ",ON\r"))
	for i in range(9):
		s.write(str.encode("$$$P10," + str(i+1) + ",ON\r"))
	# Drawing Virticle Line
	for i in range(14):
		s.write(str.encode("$$$P" + str(i+1) + ",5,ON\r"))
# $$$P1,1,ON\r)

# lights 2x2 based on the pos of the first pixel
def boxDraw(x,y):
	for i in range(2):
		s.write(str.encode("$$$P" + str(x+i) +","+ str(y) + "ON\r"))
		s.write(str.encode("$$$P" + str(x+i) +","+ str(y) + "ON\r"))
	#for i in range(2):
		s.write(str.encode("$$$P" + str(x) + "," + str(y+1) + "ON\r"))
		s.write(str.encode("$$$P" + str(x+1) + "," + str(y+1) + "ON\r"))
def boxCo(loc):
	coords = boxPos[loc].split('.')
	boxDraw(int(coords[0]),int(coords[1]))

# Total number of lights on the bridge
iLightCount = 6

def checkLights():
	for i in range(iLightCount):
		lStatus.append(b.get_light(i+1, 'on'))

def checkTrue(list):
	return (sum(bool(x) for x in list))
def getNames():
	for i in range (iLightCount):
		lName.append(b.get_light(i+1, 'name'))
def dateCount(year,month,day,event):
	# Date Calc
	delta = datetime.datetime(year,month,day) - datetime.datetime.now()
	print(delta.days)
	days = str(delta.days)

	# Clear display
	s.write(str.encode("$$$ALL,OFF\r"))     
	# Write Date
	s.write(str.encode(event+" in "+days+" days!"))

def currtime():
	timeRaw = datetime.datetime.now().strftime("%H:%M")
	print(timeRaw)
	s.write(str.encode(str(timeRaw)))

def insta():
	user = "maycontainvennom"
	url = 'https://www.instagram.com/' + user
	r = requests.get(url).text
	followers = re.search('"edge_followed_by":{"count":([0-9]+)}',r).group(1)
	print("Current Insta followers for "+ user +" is: " + followers)
	s.write(str.encode("IG: " + str(followers)))

def main():
	checkLights()
	getNames()
	insta()
	time.sleep(10)
	dateCount(2020,1,31,"Moving out")
	time.sleep(10)
	currtime()
	time.sleep(10)
	resetGrid()
	drawGrid()
	for i in range(iLightCount):
		print(lName[i] + " : " + str(lStatus[i]))
	for i in range(iLightCount):
		if lStatus[i] == True:
			boxCo(i)
	time.sleep(10)


while True:
	main()
