#!/usr/bin/python

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

button = 5
streak = 0
r =  11
g = 15
b = 18
dt = 0

keepRunning = 1

GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(r, GPIO.OUT);

red  = GPIO.PWM(r, 1000)
red.start(0)

while (keepRunning):
	GPIO.wait_for_edge(button, GPIO.FALLING)
	streak  = streak + 1
	print (streak)

	if (streak >= 10):
		streak = 10
		keepRunning = 0;

	dc =  1.5864**(streak) - 1
	red.ChangeDutyCycle(dc)
	sleep(.2)

print "out of the while loop"

red.stop()
GPIO.cleanup()
