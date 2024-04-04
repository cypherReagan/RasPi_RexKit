#!/usr/bin/env python3

import RPi.GPIO as GPIO
import time
import LCD1602
import LED
import KeypadPuP as KP
import ActiveBuzzer
import Password as PW
#import RFID_Reader as Reader

"""
This Alarm System program requires RexKit HW for the following:

- LEDs (Project 1)
- Active Buzzer (Project 4)
- LCD (I2C LCD1602 - Project 13)
- 4x4 Matrix Membrane (Keypad - Project 14)
- Light Sensor (HC-SR501 PIR SENSOR - Project 24)
- RFID Module (Project 30)


DEBUG_JW - TODO:
1.  (NOPE) Need to indicate multiple chars in word
    
    Feedback example: [N, Y, Y, I]
    
    
2.  (NOPE) Implement countdown timer.

3.  Password obj constructor should have option to init with given PW string

4. Implement LCD user menu. Options to setup (write RFID card), arm, disarm system.

5. Incorporate motion sensor in alarm system


The system will allow user to setup and set the system password.
The LCD will show user options and password feedback.

"""

################ DRIVER CODE START HERE ################
PIN_L1 = 12 #Pin BCM18 
PIN_L2 = 16 #Pin BCM23 
PIN_L3 = 18 #Pin BCM24
PIN_L4 = 22 #Pin BCM25

PIN_C1 = 19 #Pin BCM10
PIN_C2 = 15 #Pin BCM22
PIN_C3 = 13 #Pin BCM27
PIN_C4 = 11 #Pin BCM17

ROW_PINS = [PIN_L1,PIN_L2,PIN_L3,PIN_L4]
COL_PINS = [PIN_C1,PIN_C2,PIN_C3,PIN_C4]

LED_GREEN = 36  #the BOARD pin (BCM16) connect to LED
LED_RED = 37    #the BOARD pin (BCM26) connect to LED
BUZZER_PIN = 29 #the BOARD pin (BCM05) connect to active buzzer

ROWS = 4
COLS = 4
LENS = 4
KEYS =     ['1','2','3','A',
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D']

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
    
def processWord():
    
    done = False
    
    return done
    
def loop():
    global LED_GREEN
    global LED_RED
    
    #keypad = KP.Keypad(PW.KEYS,rowsPins,colsPins,ROWS,COLS)
    #keypad.setDebounceTime(50)
    keypad = KP.Keypad(KEYS,ROW_PINS,COL_PINS)
    
    global KeyIndex
    global LENS
    
    done = False
    tryCount = 3
    
    keypad.startReadKeys()
    
    while(not done):
        key = keypad.getKey()
        if(key != keypad.NULL):
            print("DEBUG_JW: key = ", key)
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
                    writeLCD(2, 1, "Alarm Disarmed!")
                    LED.enable(LED_GREEN)
                    print ('...Green LED ON (Pin ',LED_GREEN,')')
                    
                    done = True
                    time.sleep(5)
                    
            if (done):
                keypad.stopReadKeys()
                    
            KeyIndex = KeyIndex%LENS
    
    destroy()
            
            
if __name__ == '__main__':     # Program start from here
    try:
        setup()
        loop()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, end program.
        destroy()
