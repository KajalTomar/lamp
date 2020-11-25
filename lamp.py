#!/usr/bin/python3
import RPi.GPIO as GPIO
import time 
from datetime import datetime

GPIO.setmode(GPIO.BOARD)

# VARIABLES

# for the GPIO pins (using BOARD)
button = 5

r =  11
g = 15
b = 18

# duty time or something
dt = 0
endTime = "13:28:00"
# from 0 to 10
MIN_BRIGHTNESS = 0;
MAX_BRIGHTNESS = 10;

today = datetime.today()
now = datetime.now()
currentDate = today.strftime("%d/%m/%Y")


# open file to get current streak value 
with open('streak.txt', 'r') as streakFile:
	streak = int(streakFile.read())

streakFile.close()
#  open the stat file
statFile = open("stats.txt", "a")

# add this to the  stats file
# date | (1 if the button is pressed)
statFile.write("\n")
statFile.write(currentDate)
statFile.write("|0")

statFile.close()

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(r, GPIO.OUT);

# set up the brightness amount
brightness =  streak

if(streak > MAX_BRIGHTNESS):
	brightness = 10
elif (streak < MIN_BRIGHTNESS):
	brightness = 0

red  = GPIO.PWM(r, 1000)
red.start(1.5864**(brightness)-1)

if(streak > 0):
	streak = streak - 1

currentTime = now.strftime("%H:%M:%S")
print(currentTime)

# overwrite old streak file with the new file containing the updated streak 
newStreakFile = open('streak.txt', 'w')
newStreakFile.write(str(streak));

newStreakFile.close()

# put something here  for when to stop running (if he doesn't press the button by midnight?)

#EVERYTHING PAST THIS ONLY HAPPENS IF RYAN PRESSES THE BUTTON
GPIO.wait_for_edge(button, GPIO.FALLING) 

streak = streak + 2;

brightness = brightness + 1;

if (brightness > 10):
	brightness = 10
elif(brightness < 0):
	brightness = 0

dc =  1.5864**(brightness) - 1

updateStatFile =  open("stats.txt", "a")
updateStatFile.write('1')

updateStreakFile = open("streak.txt", "w")
updateStreakFile.write(str(streak))

updateStatFile.close()
updateStreakFile.close()

try:
	while(currentTime != endTime):
		red.ChangeDutyCycle(dc)
		time.sleep(.2)
		now = datetime.now()
		currentTime = now.strftime("%H:%M:%S")
 
except KeyboardInterrupt:
	pass

# if time is certain time then shut off 
print(currentTime)
red.stop()
GPIO.cleanup()
