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

DC_CONSTANT = 1.5864 # constant used to calculate duty cycle
# from 0 to 10
MIN_BRIGHTNESS = 1;
MAX_BRIGHTNESS = 10;

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
# GPIO SETUPS
# ----------------------------------------------

GPIO.setup(BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(R, GPIO.OUT);
   
# ----------------------------------------------
# FUNCTIONS
# ----------------------------------------------

#----------------------------------------------------------
# readStreak
#
# PURPOSE: reads the streak file to get the streak at the
# start of the day.
# OUTPUT: the current streak (int)
#----------------------------------------------------------
def readStreak():
	# open file to get current streak value 
	streakFile = open('streak.txt', 'r') 
	strk = int(streakFile.read())
	streakFile.close()
	return strk

#-----------------------------------------------------------
# writeToStat
#
# PURPOSE: appends the input 'item' to the end of the 
# statFile.
# INPUT: str 'item' to be appended
#-----------------------------------------------------------
def writeToStat(item):
	statFile = open("stats.txt", "a")
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
	newStreakFile = open('streak.txt', 'w')
	newStreakFile.write(strk);
	newStreakFile.close()

#------------------------------------------------------------
# setBrightness
#
# PURPOSE: sets the initial (before button is pressed)
# brightness for the lamp.
# INPUT: the current streak (int)
# OUTPUT: the brightness level (int)
#------------------------------------------------------------
def setBrightness(strk):
	bright =  strk
	if(streak > MAX_BRIGHTNESS):
		bright = MAX_BRIGTHNESS
	elif (streak < MIN_BRIGHTNESS):
		bright = MIN_BRIGHTNESS
	return bright

#------------------------------------------------------------
# updateBrightness
#
# PURPOSE: increases the brightness because the button got
# pressed!
# INPUT: the current brightness (int).
# OUTPUT: the new updated brightness.
#-------------------------------------------------------------
def updateBrightness(currentBright):
	bright = currentBright + 1;

	if (bright > MAX_BRIGHTNESS):
		bright = MAX_BRIGHTNESS
	elif(bright < MIN_BRIGHTNESS):
		bright = MIN_BRIGHTNESS

	return bright

#-------------------------------------------------------------
# calculateDutyCycle
#
# PURPOSE: Calculates the duty cycle for the PWM.
# INPUT: brightness (int) (used for calculation)
# OUTPUT: dc = duty cycle (int)
#--------------------------------------------------------------
def calculateDutyCycle(bright):
	dc = DC_CONSTANT**(bright) - 1
	return dc

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

# write this everyday
# year/month/day|0
writeToStat("\n")
writeToStat(currentDate)
writeToStat("|0")

# read the current streak
streak = readStreak()

# set up the brightness amount based on current streak
brightness =  setBrightness(streak)

# subtract one from streak (this will get fixed if Ryan pressed
# the button.
if(streak > 0):
	streak = streak - 1

# update the streak file to one less just in case Ryan doesn't 
# press the button today
writeToStreak(str(streak))

# calculate PWM and turn on LED!
dutyCycle = calculateDutyCycle(brightness)
red  = GPIO.PWM(R, 1000)
red.start(dutyCycle)

# just wait for Ryan to press the button
GPIO.wait_for_edge(BUTTON, GPIO.FALLING) 

##### EVERYTHING PAST THIS ONLY HAPPENS IF RYAN PRESSES THE BUTTON ######

# update these values to reflect button pressed
streak = streak + 2;
brightness =  updateBrightness(brightness)
dutyCycle = calculateDutyCycle(brightness)

# update the files that Ryan pressed the button!
writeToStat('1')
writeToStreak(str(streak))

# make the lamp brighter!
# keep the lamp on unless it is TURN_OFF_TIME or I ctrl+C
try:
	while(whatTime() != TURN_OFF_TIME):
		red.ChangeDutyCycle(dutyCycle)
		time.sleep(.2) 
except KeyboardInterrupt:
	pass

red.stop()
GPIO.cleanup()
