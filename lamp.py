#!/usr/bin/python3
import RPi.GPIO as GPIO
import time 
from datetime import datetime

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
# ----------------------------------------------
# VARIABLES
# ----------------------------------------------

# ------------------------
# CONSTANTS

TURN_OFF_TIME = "22:00:00" # military time

# Ryan has 14 hours (50,400,000 milliseconds) to press the button
# if we want the lamp to be on from 8am to 10 pm
TIME_TO_PRESS = 50400000
# -----------------------

# for the GPIO pins (using BOARD)
BUTTON = 5
R =  11 # red
G = 15 # green
B = 18 # blue

# date and time
today = datetime.today()
currentDate = today.strftime("%d/%m/%Y")

# ----------------------------------------------
# FUNCTIONS
# ----------------------------------------------

def setup():
	GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

	GPIO.setup(R, GPIO.OUT)
	GPIO.setup(G, GPIO.OUT)
	GPIO.setup(B, GPIO.OUT)
#----------------------------------------------------------
# readStreak
#
# PURPOSE: reads the streak file to get the streak at the
# start of the day.
# OUTPUT: the current streak (int)
#----------------------------------------------------------
def readStreak():
	# open file to get current streak value 
	streakFile = open('/var/www/html/streak.txt', 'r') 
	strk = int(streakFile.read())
	streakFile.close()

	# streak can't be negative
	if(strk < 0):
		strk = 0

	return strk

#-----------------------------------------------------------
# writeToStat
#
# PURPOSE: appends the input 'item' to the end of the 
# statFile.
# INPUT: str 'item' to be appended
#-----------------------------------------------------------
def writeToStat(item):
	statFile = open("/var/www/html/stats.txt", "a")
	# add this to the  stats file
	statFile.write(item)
	statFile.close()

#-----------------------------------------------------------
# writeToStreak
#
# PURPOSE: overwrites whatever is in the streak file (prev 
# streak) to the new steak.
# INPUT: str 'strk' which is the streak value to write.
#-----------------------------------------------------------
def writeToStreak(strk): 
	newStreakFile = open('/var/www/html/streak.txt', 'w')
	newStreakFile.write(strk);
	newStreakFile.close()

def changeColour(color):
	red.stop()
	green.stop()
	blue.stop()
	
	if(color=='yellow'):
		# yellow
		red.start(100)
		green.start(20)
	elif(color=='orange'):
		#orange
		red.start(100)
		green.start(2)
	elif(color=='pink'):
		#pink
		red.start(100)
		blue.start(1)
	elif(color=='red'):
		#red
		red.start(70)
#--------------------------------------------------------------
# whatTime
#
# PURPOSE: returns the current time.
# OUTPUT:  current time (str)
#--------------------------------------------------------------
def whatTime():
	now = datetime.now()
	currentTime = now.strftime("%H:%M:%S")
	return currentTime

# ----------------------------------------------
# MAIN SCRIPT
# ----------------------------------------------

setup()

# write this everyday
# year/month/day
writeToStat(currentDate)

# read the current streak
streak = readStreak()
print("streak: "+ str(streak))

# set the lamp to initial colors
red  = GPIO.PWM(R, 1000)
blue  = GPIO.PWM(B, 1000)
green = GPIO.PWM(G, 1000) 

if (streak == 1):
	changeColour('yellow')
elif (streak == 2):
	changeColour('orange')
elif(streak >= 3):
	changeColour('red')

# just wait for Ryan to press the button for 14 hours
button = GPIO.wait_for_edge(BUTTON, GPIO.FALLING, timeout = TIME_TO_PRESS)
if button is None:
	# IF THE BUTTON IS *NOT* PRESSED
	writeToStat('|0|00:00:00\n')
	writeToStreak('0')
	print("The button was not pressed.")
	red.stop()
	blue.stop()
	green.stop()

	GPIO.cleanup()
else:
	##### EVERYTHING PAST THIS ONLY HAPPENS IF RYAN PRESSES THE BUTTON ######
	timePressed = whatTime()

	# update these values to reflect button pressed
	streak += 1
	
	print("Button pressed.")
	print("New streak: " + str(streak))
	
	# update the files that Ryan pressed the button!
	writeToStat('|1|'+str(timePressed)+'\n')
	writeToStreak(str(streak))

	# update the color of the lamp!
	# keep the lamp on unless it is TURN_OFF_TIME or I ctrl+C
	try:
		if(streak >= 3):
		  	changeColour('pink')
			time.sleep(1)
		while(whatTime() != TURN_OFF_TIME):
			if (streak == 1):
        			changeColour('yellow')
			elif (streak == 2):
        			changeColour('orange')
			elif(streak >= 3):
				changeColour('red')
			time.sleep(.3)
	except KeyboardInterrupt:
		pass

	red.stop()
	blue.stop()
	green.stop()

	GPIO.cleanup()

