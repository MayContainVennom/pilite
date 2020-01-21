import datetime
import sys
import serial
import time
import requests
import re



s= serial.Serial()
s.baudrate = 9600
s.timeout = 0
s.port = "/dev/ttyAMA0"

try:
    s.open()
except serial.SerialException, e:
    sys.stderr.write("could not open port &r: %s\n" % (port, e))
    sys.exit(1)

def dateCount(year,month,day,event):
	# Date Calc
	delta = datetime.datetime(year,month,day) - datetime.datetime.now()
	print(delta.days)
	days = str(delta.days)

	# Clear display
	s.write("$$$ALL,OFF\r")     
	# Write Date
	s.write(event+" in "+days+" days!")

def currtime():
	timeRaw = datetime.datetime.now().strftime("%H:%M")
	print(timeRaw)
	s.write(str(timeRaw))

def insta():
	user = "maycontainvennom"
	url = 'https://www.instagram.com/' + user
	r = requests.get(url).text
	followers = re.search('"edge_followed_by":{"count":([0-9]+)}',r).group(1)
	print("Current Insta followers for "+ user +" is: " + followers)
	s.write("IG: " + str(followers))

def main():
	insta()
	time.sleep(10)
	dateCount(2020,1,31,"Moving out")
	time.sleep(10)
	currtime()
	time.sleep(10)

while True:
	main()
