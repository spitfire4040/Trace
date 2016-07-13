# import libraries
import sys
import os
import time
import datetime

# set flag variables
yearflag = False
monthflag = False
dayflag = False
uet = 0

# prompt for date
while (yearflag == False):
	os.system('clear')
	year = int(input("Enter desired year as an integer value between 2010 and 2016: "))
	if (year >= 2010 and year <= 2016):
		yearflag = True
		y = str(year)

while (monthflag == False):
	os.system('clear')
	month = int(input("Enter desired month as an integer value between 1 and 12: "))
	if (month >= 1 and month <= 12):
		monthflag = True
		if (month < 10):
			m = '0' + str(month)
		else:
			m = str(month)

while (dayflag == False):
	os.system('clear')
	day = int(input("Enter desired day as an integer value between 1 and 31: "))
	if (day >= 1 and day <= 31):
		dayflag = True
		if (day < 10):
			d = '0' + str(day)
		else:
			d = str(day)

# convert date to unix timestamp (4pm)
s = d + '/' + m + '/' + y
t = time.mktime(datetime.datetime.strptime(s, "%d/%m/%Y").timetuple())
uet = int(t) + 32400

# print date to screen
os.system('clear')
print ("Collecting data for " + m + '/' + d + '/' + y)
print (' ')

# update start time for ripe
f = open("start_time.txt", "w")
f.write(str(uet))
f.close()

	# run script syscalls

try:
	print "Working Ripe..."
	os.system("python ripe.py")
except:
	print "No Ripe data for this day"
	print " "


ark_params = "python3.5 arkparse.py " + y + ' ' + m + ' ' + d
try:
	print ("Working Ark...")
	os.system(ark_params)
except:
	print ("No Ark data for this day")
	print (" ")


mlab_params = "sudo python mlab.py " + y + ' ' + m + ' ' + d
try:
	print "Working Mlab..."
	os.system(mlab_params)
except:
	print "No MLab data for this day"
	print " "


iplane_params = "python iplane_trace.py " + y + ' ' + m + ' ' + d
try:
	print "Working iPlane..."
	os.system(iplane_params)
except:
	print "No iPlane data for this day"
	print " "