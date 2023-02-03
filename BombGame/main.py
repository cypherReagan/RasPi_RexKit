#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import LCD1602
import LED
import Keypad as KP
import ActiveBuzzer
import Password as PW

"""
This program requires RexKit HW for the following:

- LEDs (Project 1)
- Active Buzzer (Project 4)
- LCD (I2C LCD1602 - Project 13)
- 4x4 Matrix Membrane (Keypad - Project 14)


DEBUG_JW - TODO:
1.  Need to indicate multiple chars in word
    
    Feedback example: [N, Y, Y, I]
    
    
2.  Implement countdown timer.

3.  Password obj constructor should have option to intit with given PW string
"""

################ DRIVER CODE START HERE ################
LED_GREEN = 36  #the BOARD pin (BCM16) connect to LED
LED_RED = 37    #the BOARD pin (BCM26) connect to LED
BUZZER_PIN = 29 #the BOARD pin (BCM05) connect to active buzzer

ROWS = 4
COLS = 4
LENS = 4

passwordTest=['1','9','7','4']
ThePassword = PW.Password(LENS, PW.KEYS)
Testword=['0','0','0','0']
KeyIndex=0
# Keypad pins
rowsPins = [12,16,18,22] #BOARD pin numbering
colsPins = [19,15,13,11]

BUZZER_TIMEOUT = 5

def checkPW_test():
    for i in range(0,LENS):
        if(passwordTest[i]!=Testword[i]):
            return 0
    return 1

def checkPW():
    resultWord = ThePassword.getCompareResult(Testword)
    retNum = 0
    retWord = "["
    
    if (PW.IsCorrectResult(resultWord)):
        retNum = 1
        
    # make it look good
    for i in range(0, len(resultWord)):
        retWord += resultWord[i]
        if (i < len(resultWord)-1):
            retWord += ", "
    
    retWord += ']'
    
    return retNum, retWord

def setup():
    LED.setup()
    LED.init(LED_GREEN)
    LED.init(LED_RED)
    ActiveBuzzer.setup(BUZZER_PIN)
    
    LCD1602.init(0x27, 1)    # init(slave address, background light)
    LCD1602.clear()
    writeLCD(0, 0, 'WELCOME!')
    writeLCD(2, 1, 'Enter password')
    time.sleep(2)

def clearLEDs():
    LED.clear(LED_GREEN)
    LED.clear(LED_RED)

def clearHW():
    LCD1602.clear()
    clearLEDs()
    ActiveBuzzer.clear(BUZZER_PIN)
    
def destroy():
    print("--- Program Terminated ---")
    clearHW()
    # Release resource(s)
    GPIO.cleanup()
    
def writeLCD(xPos, yPos, msgStr):
    LCD1602.write(xPos, yPos, msgStr)
    print(msgStr)
    
def loop():
    global LED_GREEN
    global LED_RED
    
    keypad = KP.Keypad(PW.KEYS,rowsPins,colsPins,ROWS,COLS)
    keypad.setDebounceTime(50)
    
    global KeyIndex
    global LENS
    
    done = False
    tryCount = 3
    
    while(not done):
        key = keypad.getKey()
        if(key != keypad.NULL):
            clearHW()
            writeLCD(0, 0, "Enter :")
            writeLCD(15-KeyIndex,1, "****")
            Testword[KeyIndex]=key
            KeyIndex+=1
            if (KeyIndex is LENS):
                resultNum, resultWord = checkPW()
                if (resultNum == 0):
                    LED.enable(LED_RED)
                    LCD1602.clear()
                    #writeLCD(3, 0, "WRONG KEY!")
                    writeLCD(2, 0, resultWord)

                    tryCount = tryCount - 1
                    if (tryCount == 0):
                        ActiveBuzzer.Activate(BUZZER_PIN, BUZZER_TIMEOUT)
                        done = True
                    else:
                        msgStr = "{} {}".format("tries left: ", tryCount)
                        writeLCD(0, 1, msgStr)
                    
                else:
                    LCD1602.clear()
                    writeLCD(4, 0, "CORRECT!")
                    writeLCD(2, 1, "Bomb Disarmed!")
                    LED.enable(LED_GREEN)
                    print ('...Green LED ON (Pin ',LED_GREEN,')')
                    
                    done = True
                    time.sleep(5)
            KeyIndex = KeyIndex%LENS
    
    destroy()
            
            
if __name__ == '__main__':     # Program start from here
    try:
        setup()
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, end program.
        destroy()