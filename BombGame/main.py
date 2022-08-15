#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import LCD1602
import LED
import Keypad as KP
import ActiveBuzzer

"""
This program requires RexKit HW for the following:

- LEDs (Project 1)
- Active Buzzer (Project 4)
- LCD (I2C LCD1602 - Project 13)
- 4x4 Matrix Membrane (Keypad - Project 14)


DEBUG_JW - TODO:
1.  Create more complexity by randomly generating PW,
    allowing more tries, and giving fedback after each try.
    
    Feedback example: [X, C, C, X]
"""

################ DRIVER CODE START HERE ################
LED_GREEN = 36  #the BOARD pin (BCM16) connect to LED
LED_RED = 37    #the BOARD pin (BCM26) connect to LED
BUZZER_PIN = 29 #the BOARD pin (BCM05) connect to active buzzer

ROWS = 4
COLS = 4
LENS = 4
keys =     ['1','2','3','A',
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D']
password=['1','9','7','4']
testword=['0','0','0','0']
KeyIndex=0

# Keypad pins
rowsPins = [12,16,18,22] #BOARD pin numbering
colsPins = [19,15,13,11]

def checkPW():
    for i in range(0,LENS):
        if(password[i]!=testword[i]):
            return 0
    return 1

def setup():
    LED.setup()
    LED.init(LED_GREEN)
    LED.init(LED_RED)
    LED.enable(LED_GREEN)
    LED.enable(LED_RED)
    ActiveBuzzer.setup(BUZZER_PIN)
    
    LCD1602.init(0x27, 1)    # init(slave address, background light)
    LCD1602.clear()
    writeLCD(0, 0, 'WELCOME!')
    writeLCD(2, 1, 'Enter password')
    time.sleep(2)

def clearLEDs():
    GPIO.output(LED_GREEN, GPIO.HIGH)
    GPIO.output(LED_RED, GPIO.HIGH)

def clearHW():
    LCD1602.clear()
    clearLEDs()
    ActiveBuzzer.clear(BUZZER_PIN)
    
def writeLCD(xPos, yPos, msgStr):
    LCD1602.write(xPos, yPos, msgStr)
    print(msgStr)
    
def loop():
    global LED_GREEN
    global LED_RED
    
    keypad = KP.Keypad(keys,rowsPins,colsPins,ROWS,COLS)
    keypad.setDebounceTime(50)
    
    global KeyIndex
    global LENS
    
    while(True):
        key = keypad.getKey()
        if(key != keypad.NULL):
            clearHW()
            writeLCD(0, 0, "Enter password:")
            writeLCD(15-KeyIndex,1, "****")
            testword[KeyIndex]=key
            KeyIndex+=1
            if (KeyIndex is LENS):
                if (checkPW() == 0):
                    LCD1602.clear()
                    writeLCD(3, 0, "WRONG KEY!")
                    writeLCD(0, 1, "please try again")
                    GPIO.output(LED_RED, GPIO.LOW)
                    ActiveBuzzer.Activate(BUZZER_PIN, 5)
                else:
                    LCD1602.clear()
                    writeLCD(4, 0, "CORRECT!")
                    writeLCD(2, 1, "Bomb Disarmed!")
                    GPIO.output(LED_GREEN, GPIO.LOW)
                    print ('...Green LED ON (Pin ',LED_GREEN,')')
            KeyIndex = KeyIndex%LENS
            
            
if __name__ == '__main__':     # Program start from here
    try:
        setup()
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the program destroy() will be  executed.
        print("--- Program Terminated ---")
        clearHW()
        # Release resource(s)
        GPIO.cleanup()