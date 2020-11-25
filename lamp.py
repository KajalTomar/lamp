#!/usr/bin/python3
import RPi.GPIO as GPIO
import time 
from datetime import datetime

GPIO.setmode(GPIO.BOARD)

# ----------------------------------------------
# VARIABLES
# ----------------------------------------------

# ------------------------
# CONSTANTS

TURN_OFF_TIME = "13:28:00" # military time

# from 0 to 10
MIN_BRIGHTNESS = 0;
MAX_BRIGHTNESS = 10;

# -----------------------

# for the GPIO pins (using BOARD)
BUTTON = 5
R =  11 # red
G = 15 # green
B = 18 # blue

# for changing the brightness
dutyCycle 
streak
brightness

# date and time
today = datetime.today()
currentDate = today.strftime("%d/%m/%Y")

# colours
red
blue
green

# ----------------------------------------------
# GPIO setups
# ----------------------------------------------

GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(R, GPIO.OUT);
   
# ----------------------------------------------
# Functions
# ----------------------------------------------

def readStreak():
	# open file to get current streak value 
	strk
	with open('streak.txt', 'r') as streakFile:
		strk = int(streakFile.read())
	streakFile.close()
	return strk

def writeToStat(item):
	statFile = open("stats.txt", "a")
	# add this to the  stats file
	statFile.write(item)
	statFile.close()

def writeToStreak(strk):
	# overwrite old streak file with the new file containing the updated streak 
	newStreakFile = open('streak.txt', 'w')
	newStreakFile.write(str(strk));
	streakFile.close()
	
def setBrightness(strk):
	bright =  strk
	if(streak > MAX_BRIGHTNESS):
		bright = 10
	elif (streak < MIN_BRIGHTNESS):
		bright = 0
	return bright

def updateBrightness(currentBright):
	bright = currentBright + 1;

	if (bright > 10):
		bright = 10
	elif(bright < 0):
		bright = 0
	
	return bright
	
def calculateDutyCycle(bright):
	dc = 1.5864**(bright) - 1
	return dc

def whatTime():
	now = datetime.now()
	currentTime = now.strftime("%H:%M:%S")
	return currentTime

# ----------------------------------------------
# Main script
# ----------------------------------------------

# write this everyday
writeToStat("n")
writeToStat(currentDate)
writeToStat("|0")

streak = readStreak()
# set up the brightness amount
brightness =  setBrightness(streak)

if(streak > 0):
	streak = streak - 1

# update the streak to one less just in case Ryan doesn't press the button today
writeToStreak(streak)

dutyCycle = calculateDutyCycle(brightness)
red  = GPIO.PWM(r, 1000)
red.start(dutyCycle)

GPIO.wait_for_edge(button, GPIO.FALLING) 
##### EVERYTHING PAST THIS ONLY HAPPENS IF RYAN PRESSES THE BUTTON ######

# update these values to reflect button pressed
streak = streak + 2;
brightness =  updateBrightness(brightness)
dutyCycle = calculateDutyCycle(brightness)

# update the files that Ryan pressed the button!
writeToStat('1')
writeToStreak(str(streak))

try:
	while(whatTime() != TURN_OFF_TIME):
		red.ChangeDutyCycle(dutyCycle)
		time.sleep(.2) 
except KeyboardInterrupt:
	pass

red.stop()
GPIO.cleanup()
