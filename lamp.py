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

DC_CONSTANT = 4.62606500918 # 4.64158834 # constant used to calculate duty cycle

# from 1 to 3
MIN_BRIGHTNESS = 0
MAX_BRIGHTNESS = 3

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
		bright = MAX_BRIGHTNESS
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
	dc = DC_CONSTANT**(bright)-1
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

setup()

# write this everyday
# year/month/day
writeToStat(currentDate)

# read the current streak
streak = readStreak()
print("streak: "+ str(streak))
# set up the brightness amount based on current streak
brightness =  setBrightness(streak)

# calculate PWM and turn on LED!
dutyCycle = calculateDutyCycle(brightness)

red  = GPIO.PWM(R, 1000)
blue  = GPIO.PWM(B, 1000)

print("dutycycle: "+ str(dutyCycle))

if (streak < 3):
	red.start(dutyCycle)
elif (streak >= 3):
	blue.start(dutyCycle)

# just wait for Ryan to press the button
button = GPIO.wait_for_edge(BUTTON, GPIO.FALLING, timeout = 60000) 
if button is None:
	#WHEN THE BUTTON IS *NOT* PRESSED
	writeToStat('|0\n')
	writeToStreak('0')
	print("The button was not pressed.")
       	red.stop()
        blue.stop()
        green.stop()

        GPIO.cleanup()
else:
	##### EVERYTHING PAST THIS ONLY HAPPENS IF RYAN PRESSES THE BUTTON ######
	green = GPIO.PWM(G, 1000)
	# update these values to reflect button pressed
	streak += 1

	brightness =  updateBrightness(brightness)
	dutyCycle = calculateDutyCycle(brightness)

	print("Button pressed.")
	print("New streak: " + str(streak))
	# update the files that Ryan pressed the button!
	writeToStat('|1\n')
	writeToStreak(str(streak))

	# make the lamp brighter!
	# keep the lamp on unless it is TURN_OFF_TIME or I ctrl+C

	print("dutyCycle: " + str(dutyCycle))
	try:
		while(whatTime() != TURN_OFF_TIME):
			if(streak < 3):
				red.ChangeDutyCycle(dutyCycle)
			elif(streak == 3):
				green.start(2)
				green.ChangeDutyCycle(dutyCycle)
				time.sleep(1.0)
				blue.start(dutyCycle)
			else:	
				#for count in range(0,40):
				blue.ChangeDutyCycle(dutyCycle)
			time.sleep(.3)
	except KeyboardInterrupt:
		pass

	red.stop()
	blue.stop()
	green.stop()

	GPIO.cleanup()

