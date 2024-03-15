# import required libraries
import RPi.GPIO as GPIO
import time

# https://www.digikey.com/en/maker/blogs/2021/how-to-connect-a-keypad-to-a-raspberry-pi

# Pins for Raspi4
GPIO_MODE = GPIO.BCM
PIN_L1 = 18 #Pin 12 on board 
PIN_L2 = 23 #Pin 16 on board 
PIN_L3 = 24 #Pin 18 on board 
PIN_L4 = 25 #Pin 22 on board

PIN_C1 = 10 #Pin 19 on board
PIN_C2 = 22 #Pin 15 on board
PIN_C3 = 27 #Pin 13 on board
PIN_C4 = 17 #Pin 11 on board

ROW_PINS = [PIN_L1,PIN_L2,PIN_L3,PIN_L4]
COL_PINS = [PIN_C1,PIN_C2,PIN_C3,PIN_C4]

HOLD_TIME = 0.3
TESTMODE = True
ROWS = 4
COLS = 4
LENS = 4
keys =     ['1','2','3','A',
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D']
password=['1','9','7','4']
testword=['0','0','0','0']


class Keypad(object):
    NULL = '\0'
    LIST_MAX = 10   #Max number of keys on the active list.
    MAPSIZE = 10    #MAPSIZE is the number of rows (times 16 columns)
    bitMap = [0]*MAPSIZE
    ##key = [Key()]*LIST_MAX
    holdTime = 500        #key hold time
    holdTimer = 0
    startTime = 0
    
    #Allows custom keymap, pin configuration, and keypad sizes.
    def __init__(self,usrKeyMap,rowPins,colPins):
        self.__rowPins = rowPins
        self.__colPins = colPins
        self.__numRows = len(rowPins)
        self.__numCols = len(colPins)
        self.__keymap = usrKeyMap
        #DEBUG_JW: TODO - add queue for entered keys
        
        self.__setupHw()


    # init the GPIO pins
    # rowPins/colPins must already be initialized
    def __setupHw(self):
        GPIO.setmode(GPIO_MODE)
        GPIO.setwarnings(False)
        
        for rowPin in self.__rowPins:
            GPIO.setup(rowPin, GPIO.OUT)
            
        # MUST configure the input pins to use the internal pull-down resistors
        for colPin in self.__colPins:
            GPIO.setup(colPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    # Function sends out a single pulse to one of the rows of the keypad
    # and then checks each column for changes.
    # If it detects a change, the user pressed the button that connects the given line
    # to the detected column.

    def readLine(self, rowPin, characters):
        
        retChar = ""
        GPIO.output(rowPin, GPIO.HIGH)

        for i in range (0, self.__numCols):
            if(GPIO.input(self.__colPins[i]) == 1):
                retChar = (characters[i])
                 
        
        GPIO.output(rowPin, GPIO.LOW)   
        
        return retChar
    
    #Returns a single key only. Retained for backwards compatibility.
    #def getKey(self):
        
    
################ SIMPLE KEYPAD START HERE ################


def testSetup_OLD():  
    print('WELCOME to the simple keypad!')
    print('Enter password')
    time.sleep(2)
    # Initialize the GPIO pins

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO_MODE)

    GPIO.setup(L1, GPIO.OUT)
    GPIO.setup(L2, GPIO.OUT)
    GPIO.setup(L3, GPIO.OUT)
    GPIO.setup(L4, GPIO.OUT)

    # Make sure to configure the input pins to use the internal pull-down resistors

    GPIO.setup(C1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(C4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def readLine_OLD(line, characters):
    
    retChar = ""
    GPIO.output(line, GPIO.HIGH)
    if(GPIO.input(C1) == 1):
        retChar = (characters[0])
    if(GPIO.input(C2) == 1):
        retChar = (characters[1])
    if(GPIO.input(C3) == 1):
        retChar = (characters[2])
    if(GPIO.input(C4) == 1):
        retChar = (characters[3])
    GPIO.output(line, GPIO.LOW)
    
    return retChar


def simpleTestLoop(keypad):
    while True:
        # call the readLine function for each row of the keypad
        char = keypad.readLine(ROW_PINS[0], ["1","2","3","A"])
        if (not char == ""):
            print(char)
        
        char = keypad.readLine(ROW_PINS[1], ["4","5","6","B"])
        if (not char == ""):
            print(char)
        
        char = keypad.readLine(ROW_PINS[2], ["7","8","9","C"])
        if (not char == ""):
            print(char)
        
        char = keypad.readLine(ROW_PINS[3], ["*","0","#","D"])
        if (not char == ""):
            print(char)

        
        #print (readLine(L1, ["1","2","3","A"]))
        #print (readLine(L2, ["4","5","6","B"]))
        #print (readLine(L3, ["7","8","9","C"]))
        #print (readLine(L4, ["*","0","#","D"]))
        ##time.sleep(0.1)
        time.sleep(HOLD_TIME)
 
        
def destroy(testMode = False):
    print('KeyPad Destroy')
    
    if (testMode):
        # Release resource
        GPIO.cleanup()
    
if __name__ == '__main__':     # Program start from here
    try:
        print('WELCOME to the simple keypad!')
        print('Enter password')
        time.sleep(2)
        keypad = Keypad(keys,ROW_PINS,COL_PINS)
        simpleTestLoop(keypad)
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the program destroy() will be  executed.
        destroy(TESTMODE)