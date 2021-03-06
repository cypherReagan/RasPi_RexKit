#!/usr/bin/env python3
import RPi.GPIO as GPIO  #the pin libaray of raspberry
import time  #the time libaray of system time
TestLedPin1 = 36  #the BOARD pin (BCM16) connect to LED
TestLedPin2 = 37  #the BOARD pin (BCM26) connect to LED

def setup(testMode = False):
    # Set the GPIO modes to BCM Numbering
    #DEBUG_JW - removed for now
    GPIO.setmode(GPIO.BOARD)
    
    if (testMode):
        init(TestLedPin1)
        init(TestLedPin2)
    

def init(ledPin):
    # Set LedPin's mode to output,and initial level to High(3.3v)
    print("Init GPIO pin ", ledPin)
    GPIO.setup(ledPin, GPIO.OUT, initial=GPIO.HIGH)
    
def loop(ledPin, testMode = True):
    while True:
        print ('...LED ON')
        # Turn on LED
        if (testMode):
            GPIO.output(TestLedPin1, GPIO.LOW)
            GPIO.output(TestLedPin2, GPIO.LOW)
        else:
            GPIO.output(ledPin, GPIO.LOW)
        time.sleep(1)
        
        print ('LED OFF...')
        # Turn off LED
        if (testMode):
            GPIO.output(TestLedPin1, GPIO.HIGH)
            GPIO.output(TestLedPin2, GPIO.HIGH)
        else:
            GPIO.output(ledPin, GPIO.HIGH)
        time.sleep(1)

# Define a main function for main process
def main():
    x = 1

# Define a enable function to turn on LED
def enable(ledPin):
    # Turn off LED
    GPIO.output(ledPin, GPIO.HIGH)

# Define a destroy function to turn off LED
def clear(ledPin):
    # Turn off LED
    GPIO.output(ledPin, GPIO.HIGH)

# Define a destroy function for clean up everything after the script finished
def destroy(ledPin, testMode = True):
    # Turn off LED
    if (testMode):
        clear(TestLedPin1)
        clear(TestLedPin2)
    else:
        clear(ledPin)
    # Release resource
    GPIO.cleanup()
    
# If run this script directly, do:
if __name__ == '__main__':
    setup(True)

    try:
        loop(0)

    # When 'Ctrl+C' is pressed, the program destroy() will be  executed.
    except KeyboardInterrupt:
        destroy(0)
        destroy(0)
