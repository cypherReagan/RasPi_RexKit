#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

# Set #17 as buzzer pin
testBeepPin = 29 #the BOARD pin (BCM05) connect to LED

def setup(beepPin):
	# Set the GPIO modes to BOARD Numbering
	GPIO.setmode(GPIO.BOARD)
	# Set LedPin's mode to output,
	# and initial level to High(3.3v)
	GPIO.setup(beepPin, GPIO.OUT, initial=GPIO.HIGH)

def main():
	while True:
		# Buzzer on (Beep)
		print ('Buzzer On')
		GPIO.output(testBeepPin, GPIO.LOW)
		time.sleep(3)
		# Buzzer off
		print ('Buzzer Off')
		GPIO.output(testBeepPin, GPIO.HIGH)
		time.sleep(3)

def destroy(beepPin):
	# Turn off buzzer
	GPIO.output(beepPin, GPIO.HIGH)
	# Release resource
	GPIO.cleanup()

# If run this script directly, do:
if __name__ == '__main__':
	setup(testBeepPin)
	try:
		main()
	# When 'Ctrl+C' is pressed, the program
	# destroy() will be  executed.
	except KeyboardInterrupt:
		destroy(testBeepPin)