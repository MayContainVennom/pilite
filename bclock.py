import sys
import serial
import time
import datetime

s= serial.Serial()
s.baudrate = 9600
s.timeout = 0
s.port = "/dev/ttyAMA0"

#Lists for LED positions (Arrays always need to be 4 long)
lHour1 = ["2.6","0.0","2.6","2.8"]
lHour2 = ["5.2","5.4","5.6","5.8"]
lMin1 = ["10.2","10.4","10.6","10.8"]
lMin2 = ["13.2","13.4","13.6","13.8"]

try:
    s.open()
except serial.SerialException as e:
    sys.stderr.write("could not open port &r: %s\n" % (port, e))
    sys.exit(1)

def resetGrid():
	s.write(str.encode("$$$ALL,OFF\r"))

resetGrid()

def pOn(lPos):
	coords = lPos.split('.')
	s.write(str.encode("$$$P" + str(coords[0]) + "," + str(coords[1]) + "ON\r"))

def pOff(lPos):
	print(lPos)
	coords = lPos.split('.')
	s.write(str.encode("$$$P" + str(coords[0]) + "," + str(coords[1]) + "OFF\r"))


def binArray(bStrp):
	print(bStrp)
	#removing the prefix
	bStr = bStrp.split('0b')
	print(bStr[1])
	# Splitting Binary Value into an array
	bArr = list(map(int, bStr[1]))
	# Adds in missing 0's
	while len(bArr) < 4:
		bArr.insert(0,0)
		print(bArr)
	return bArr

def draw(array,lArray):
	# LED Switching
	for i in range(4):
		if array[i] == 1:
			print(str(i) + ": "+ lArray[i])
			pOn(lArray[i])
		else:
			pOff(lArray[i])
def main():
	timeRaw = datetime.datetime.now().strftime("%H%M")
	print("The time is: " + timeRaw)
	#Converts Time into an Array
	timeArr = list(map(int, timeRaw))
	print(timeArr)
	#Sets the display
	draw(binArray(bin(timeArr[0])),lHour1)
	draw(binArray(bin(timeArr[1])),lHour2)
	draw(binArray(bin(timeArr[2])),lMin1)
	draw(binArray(bin(timeArr[3])),lMin2)

while True:
		
	main()
	time.sleep(10)	
