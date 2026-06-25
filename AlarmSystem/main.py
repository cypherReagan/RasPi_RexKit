#!/usr/bin/env python3
import HwSim as HW

if (HW.RASPI):
    import RPi.GPIO as GPIO
    import LCD1602
    import LED
    import ActiveBuzzer
    #import RFID_Reader as Reader

import time
import Password as PW
import Menu
import KeypadPuP as KP

SW_REV = 0.5
# 0.1 = implementing Menu Manager to maintain and navigate menu options
# 0.2 = implemented Password class option to read/write to disk
# 0.3 = added main simulation driver code and simple PW enter test
# 0.4 = updated main simulation driver code to run system startup sequence
# 0.5 = refactored HW setup and cleanup code into HwSim. Also updated project details.
# 0.6 = code cleanup and refactored SimKey codeto prevent stale data. Also fixed some bugs in Menu code.
"""
This Alarm System program requires RexKit HW for the following:

- LEDs (Project 1)
- Active Buzzer (Project 4)
- LCD (I2C LCD1602 - Project 13)
- 4x4 Matrix Membrane (Keypad - Project 14) - using internal pull-up implementation of this
- Light Sensor (HC-SR501 PIR SENSOR - Project 24)
- RFID Module (Project 30)


DEBUG_JW - TODO:
1.  (NOPE) Need to indicate multiple chars in word
    
    Feedback example: [N, Y, Y, I]
    
2.  (NOPE) Implement countdown timer.

3.  (DONE) Password obj constructor should have option to init with given PW string

4. Implement LCD user menu. Options to setup (write RFID card), arm, disarm system, set master PW.
    |
    |-> currently writing Menu Manager to maintain and navigate menu options.

5. Incorporate motion sensor in alarm system

6. Feature to save master PW to disk
    |
    |-> partially implemented in Password class. Still need menu option.

7. Feature to use Snap Circuit alarm IC

8. Feature revoke PW (either typed or RFID)

9. Implement mobile blueDot app to arm/disarm system

10. Implement facial recognition to arm/disarm system

11. Implement Blue Dot alert when system is tripped

12. Implement camera capture when system is tripped

13. Implement SMS alert when system is tripped (Twilio) --> nope - Twilio is too expensive for our use case

14. Implement auto-lockout after 3 failed password attempts

15. Implement password entry via RFID tag

16. Implement password entry via keypad


System Flow:

The system will allow user to setup the system password.
The LCD will show user menu options (SETUP, ARM, DISARM) and password feedback.
The user can choose to arm the system after setup. Once armed, the system will be tripped when the motion sensor is triggered. 
Once tripped, the user can attempt to disarm the system by entering the correct password via the keypad or RFID tag. 
The LCD will provide feedback on password entry and indicate if the system is disarmed or if a wrong password was entered.
Once sytem is tripped, the user will have 3 attempts to enter the correct password before system lockout.

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

PW_LEN = 4

ThePassword = PW.Password(PW_LEN, PW.KEYS)

# Test code
Testword=['0','0','0','0'] #DEBUG_JW - DELETEME
passwordTest=['1','9','7','4']
Masterword=['0','0','0','0']
# end test code

# Keypad pins
ROW_PINS = [12,16,18,22] #BOARD pin numbering
COL_PINS = [19,15,13,11]
TheKeyPad = KP.Keypad(PW.KEYS,ROW_PINS,COL_PINS)

BUZZER_TIMEOUT = 5

def checkPW_test(pwLen):
    for i in range(0,pwLen):
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

# HW setup and utility functions
def setup():
    HW.setupLEDs(LED_GREEN, LED_RED)
    HW.setupBuzzer(BUZZER_PIN)
    
    HW.initLCD()
    writeLCD(0, 0, 'WELCOME!')
    writeLCD(2, 1, 'Enter password')
    time.sleep(2)

def clearLEDs():
    HW.clearLEDs(LED_GREEN, LED_RED)

def clearHW():
    HW.clearLCD()
    HW.clearLEDs(LED_GREEN, LED_RED)
    HW.clearBuzzer(BUZZER_PIN)
    
def destroy():
    print("--- Program Terminated ---")
    clearHW()
    # Release resource(s)
    HW.cleanupGpio()
    
def writeLCD(xPos, yPos, msgStr):
    HW.writeLCD(xPos, yPos, msgStr)
   
# Prompts user for the master system password.
# If successful, returns word array
#
# Assumes the keyPad has started capturing
def getMasterUserWord(keypad, pwLen=PW_LEN):

    done = False
    keyIndex = 0
    word = [''] * pwLen
    
    clearHW()
    
    promptStr = "Enter :"
    promptIndex = len(promptStr)
    writeLCD(0, 0, promptStr) # add entered key after prompt
    
    
    while(not done):
        key = keypad.getKey()
        if(key != keypad.NULL):
            writeLCD(promptIndex+keyIndex, 0, key) # add entered key after prompt
            
            word[keyIndex]=key
            keyIndex+=1
            print("DEBUG_JW: getMasterUserWord () - key = ", key, ", keyIndex = ", keyIndex)
            if (keyIndex is pwLen):
                print("DEBUG_JW: getMasterUserPw() - returning PW")
                return word
            
   
# TODO: needs major refactor
def alarmLoop(keypad, pwLen = PW_LEN):
    global LED_GREEN
    global LED_RED
    global ThePassword
    
    done = False
    tryCount = 3
    keyIndex = 0
    """"
    keypad.startReadKeys()
    masterWord = getMasterUserWord(keypad)
    ThePassword = PW.Password(LENS, PW.KEYS, masterWord)
    """
    # TODO: check if master PW exists on disk at startup
    ThePassword = SetMasterPW(keypad, ThePassword, pwLen)
    HW.clearLCD()
    
    while(not done):
        key = keypad.getKey()
        if(key != keypad.NULL):
            print("DEBUG_JW: key = ", key)
            clearHW()
            writeLCD(0, 0, "Enter:")
            writeLCD(15-keyIndex,1, "****")
            Testword[keyIndex]=key
            keyIndex+=1
            if (keyIndex is pwLen):
                resultNum, resultWord = checkPW()
                if (resultNum == 0):
                    HW.enableLED(LED_RED)
                    HW.clearLCD()
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
                    HW.clearLCD()
                    writeLCD(4, 0, "CORRECT!")
                    writeLCD(2, 1, "Alarm Disarmed!")
                    HW.enableLED(LED_GREEN)
                    print ('...Green LED ON (Pin ',LED_GREEN,')')
                    
                    done = True
                    time.sleep(5)
                    
            keyIndex = keyIndex%pwLen
            
            if (done):
                keypad.stopReadKeys()
    
# Reads user input for PW, sets pw, and saves it to disk.
#
# Returns the PW object with the new password set.     
def SetMasterPW(keypad, pw, pwLen):
    keypad.startReadKeys()
    masterWord = getMasterUserWord(keypad, pwLen)
    pw = PW.Password(pwLen, PW.KEYS, masterWord)
    pw.saveToDisk()
    return pw

# Attemps to read master system password from disk.
# If successful reads PW, returns Menu.Action.INVALID. Else returns Menu.Action.SETPW
# Returns the PW object with the read password (if successful) or unchanged PW (if unsuccessful) and the menu action to be taken.
def ReadBackMasterPW(pw):
    retAction = Menu.Action.SETPW.value

    diskPwStr = pw.readFromDisk()

    if ("" == diskPwStr):
        retAction = Menu.Action.SETPW.value

    return pw, retAction

# Invoked at system startup to read back master PW from disk. 
# If not successful, prompts user to set master PW.
def RunSystemStartUp(keypad, pw, pwLen):
    pw, action = ReadBackMasterPW(pw)

    if (action == Menu.Action.SETPW.value):
        pw = SetMasterPW(keypad,pw, pwLen)
    return pw

# ---------
# Test Code
# ---------      
def SimulationDriver(keypad, pw):
    print("--- Simulation driver ---")

    HW.SetSimKeys(['1','2','3','4']) 

    step = 1

    # STEP. Clear any saved disk password for test
    pw.clearDiskFile()

    # STEP. simulate system startup and read back any save password
    print(str(step) + ". Startup system check: Read PW")
    pw, action = ReadBackMasterPW(pw)

    if (action != Menu.Action.SETPW.value):
        print("Sim Driver ERROR: invalid action after startup. Expecting action=SETPW(" + str(Menu.Action.SETPW.value) + ") but got " + str(action))
        return

    # STEP. Set password on fresh system startup
    step += 1
    print(str(step) + ". Startup system check: Set PW")
    action = Menu.Action.SETPW.value

    pw = SetMasterPW(keypad,pw, HW.GetSimKeySize())

    # STEP. Arm system
    step += 1
    action = Menu.Action.ARM_SYSTEM.value

    print("---End of simulation driver---")
    return pw

if __name__ == '__main__':     # Program start from here
    #global ThePassword
    global TheKeypad

    print("================================")
    print("RASPI ALARM SYSTEM\nSW Rev = " + str(SW_REV))
    print("================================")

    if (not HW.RASPI):
        ThePassword = SimulationDriver(TheKeyPad, ThePassword)
    else:
        # DEBUG_JW - not ready for primetime until Menu is done
        try:
            setup()
            alarmLoop(TheKeypad)
            destroy()
        except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, end program.
            TheKeypad.stopReadKeys()
            destroy()