#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time

TESTMODE = True
# Set buzzer pin
testBeepPin = 29 #the BOARD pin (BCM05) connect to LED

def setup(beepPin):
    # Set the GPIO modes to BOARD Numbering
    GPIO.setmode(GPIO.BOARD)
    # Set LedPin's mode to output,
    # and initial level to High(3.3v)
    GPIO.setup(beepPin, GPIO.OUT, initial=GPIO.HIGH)
    print("ActiveBuzzer - Init GPIO pin ", beepPin)
    
def Activate(beepPin, timer):
    if (timer < 0):
        print("ERROR: ActiveBuzzer.Activate() - Invalid timer value!")
    else:
        print ('Buzzer On')
        GPIO.output(beepPin, GPIO.LOW)
        time.sleep(timer)
        print ('Buzzer Off')
        GPIO.output(beepPin, GPIO.HIGH)
    
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

def clear(beepPin):
    # Turn off buzzer
    GPIO.output(beepPin, GPIO.HIGH)

def destroy(beepPin, testMode = False):
    # Turn off buzzer
    GPIO.output(beepPin, GPIO.HIGH)
    
    if (testMode):
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
        destroy(testBeepPin, TESTMODE)