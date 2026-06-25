
RASPI = False # Set flag to True to enable HW and False to disable HW and run in simulation mode.

if (RASPI):
    import LCD1602
    import LED
    import ActiveBuzzer
    import RPi.GPIO as GPIO


#-------------------
# Keypad Simulation
#-------------------
__SimKeys = []
__SimKeysVersion = 0
if (not RASPI):
    # <Insert Desired Keypad Simulation Sequence Here or Use Accessors To Set Keys>
    x =1 # dummy line to allow for easy insertion of desired keypad simulation sequence.  See SetSimKeys() below.
    # Default sequence should be empty so unit tests explicitly set the desired keys.
    # Main Test example:
    # __SimKeys = ['A', 'B', 'C', '1', '2', '3'] # main PW test: pass

    # Menu Test examples:
    # __SimKeys = ['A', 'A'] # menu test: pass
    # __SimKeys = ['A', 'C', 'A'] # menu test: pass
    # __SimKeys = ['A', 'B'] # menu test: fail
    # __SimKeys = ['B'] # menu test: pass
    # __SimKeys = ['B', 'A'] # menu test: pass
    # __SimKeys = ['C', 'A', 'A'] # menu test: fail


def GetSimKeys():
    global __SimKeys
    return __SimKeys

def GetSimKeysVersion():
    global __SimKeysVersion
    return __SimKeysVersion

def SetSimKeys(keys):
    if (RASPI):
        print("ERROR: Cannot SetSimKeys when HW is enabled")
    else:
        global __SimKeys
        global __SimKeysVersion
        __SimKeys = keys
        __SimKeysVersion += 1
    
def GetSimKeySize():
    retVal = 0
    if (RASPI):
        print("ERROR: Cannot GetSimKeySize when HW is enabled")
    else:
        global __SimKeys
        retVal = len(__SimKeys)

    return retVal


#----------------
# LCD Simulation
#----------------
def initLCD():
    if (RASPI):
        LCD1602.init(0x27, 1)    # init(slave address, background light)
        LCD1602.clear()

def clearLCD():
    if (RASPI):
        LCD1602.clear()

def writeLCD(xPos, yPos, msgStr):
    
    print("#####-LCD-#####")
    if (yPos > 0):
        print("")
    print(msgStr)
    print("###############")
    
    if (RASPI):
        LCD1602.write(xPos, yPos, msgStr)


#----------------
# LED Simulation
#----------------
def setupLEDs(ledGreenPin, ledRedPin):
    if (RASPI):
        LED.setup()
        LED.init(ledGreenPin)
        LED.init(ledRedPin)

def clearLEDs(ledGreenPin, ledRedPin):
    if (RASPI):
        LED.clear(ledGreenPin)
        LED.clear(ledRedPin)

def enableLED(ledPin):
    if (RASPI):
        LED.enable(ledPin)
#----------------
# Buzzer Simulation
#----------------
def setupBuzzer(buzzerPin):
    if (RASPI):
        ActiveBuzzer.setup(buzzerPin)

def clearBuzzer(buzzerPin):
    if (RASPI):
        ActiveBuzzer.clear(buzzerPin)

#--------------------
# General Simulation
#--------------------
def init():
    initLCD()

def cleanupGpio():
    if (RASPI):
        GPIO.cleanup()
    
    
if __name__ == '__main__':     # Program start from here
    print("Test Not Implemented for Simulation")