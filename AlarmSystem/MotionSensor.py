#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

testLedPin = 18    # define the ledPin
testSensorPin = 17    # define the sensorPin
INIT_TIME = 3

def setup(mode, ledPin, sensorPin):
	print("Initializing Motion Sensor...")
	GPIO.setmode(mode)       # Numbers GPIOs by physical location
	GPIO.setup(ledPin, GPIO.OUT)   # Set ledPin's mode is output
	GPIO.setup(sensorPin, GPIO.IN)    # Set sensorPin's mode is input
	time.sleep(INIT_TIME)

def testLoop():
    #TODO: factor in 3 sec OFF delay adjustment
	while True:
		if GPIO.input(testSensorPin)==GPIO.HIGH:
			GPIO.output(testLedPin,GPIO.HIGH)
			print ('led on ...')
		else :
			GPIO.output(testLedPin,GPIO.LOW)
			print ('led off ...')
			
def loop(ledPin, sensorPin):
    #TODO: factor in 3 sec OFF delay adjustment
	while True:
		if GPIO.input(sensorPin)==GPIO.HIGH:
			GPIO.output(ledPin,GPIO.HIGH)
			print ('led on ...')
		else :
			GPIO.output(ledPin,GPIO.LOW)
			print ('led off ...')

def destroy():
	GPIO.cleanup()             # Release resource
	print ('Goodbye')

if __name__ == '__main__':     # Program start from here
    print("--- Running motion sensor test ---")
    setup(GPIO.BCM, testLedPin, testSensorPin)
    try:
        testLoop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
        destroy()


