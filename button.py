#!/usr/bin/python3
import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

def button_callback(channel):
    print("Button was pushed!")

button = 5;
GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 10 to be an input pin and set initial value to be pulled low (off)

#GPIO.add_event_detect(5, GPIO.RISING, callback=button_callback, bouncetime=1000)

button = GPIO.wait_for_edge(button, GPIO.RISING, timeout=60000)
if button is None:
	print("you didn't press the button")
else:
	print("the button was pressed in time!")

message = input("Press enter to quit\n\n") # Run until someone presses enter
GPIO.cleanup() # Clean up

