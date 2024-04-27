import time
import LCD1602
import KeypadPuP as KP

"""
Possible Options:

1. Set Master PW
2. Setup RFID card
3. Arm/Disarm System
"""

SelectChar = 'A'
BackChar = 'B'
NextChar = 'C'
PrevChar = 'D'

# Shows the options on the LCD and captures selections.
# Returns index if the user selected valid option
# Returns -1 if options are invalid
# Returns -2 if user quits without selecting option
#
# Assumes the keyPad has started capturing
def RunOptions(menuTitle, options, keyPad):
    
    retVal = -1
    index = 0
    done = False
    optCount = len(options)
    if (optCount is 0):
        print("ERROR: RunOptions() - invalid options arg")
    else:
    
        increment = 0
        
        while (not done):
        #for entry in options:
            if (index >= len(options)):
                # reset to 1st option
                index = 0
                
            if (index < 0):
                # reset to 1st option
                index = len(options) - 1
                
            entry = options[index]
                
            writeLCD(0, 0, menuTitle)
            msg = "{}. ".format(index+1) + entry
            
            writeLCD(0, 1, msg)
            
            # wait for user input
            key = keyPad.NULL
            while (key is keyPad.NULL):
                key = keyPad.getKey()
                
                if (key is SelectChar):
                    # capture our selection
                    retVal = index
                    done = True
                    break
                elif (key is NextChar):
                    # go to next option
                    increment = 1
                    break
                elif (key is PrevChar):
                    # go to previous option
                    increment = -1
                    break
                elif (key is BackChar):
                    # user quits
                    retVal = -2
                    done = True
                    break
                
            index += increment
            LCD1602.clear()

    return retVal

# ---------
# Test Code
# ---------
TestKeyPad = KP.Keypad(KP.KEYS,KP.ROW_PINS,KP.COL_PINS)

TEST_OPTIONS1 = ["Set Master PW",
                 "Setup Card",
                 "Arm System",
                 "Disarm System"]

TEST_OPTIONS2 = ["Set PW1",
                 "Set PW2"]

MENU_NAMES = ["Options1", "Options2"]
MENUS = [TEST_OPTIONS1, TEST_OPTIONS2]

def setup():
    
    LCD1602.init(0x27, 1)    # init(slave address, background light)
    LCD1602.clear()

def writeLCD(xPos, yPos, msgStr):
    LCD1602.write(xPos, yPos, msgStr)
    print(msgStr)

def destroy():
    print("--- Menu Test Terminated By User ---")
    LCD1602.clear()



if __name__ == '__main__':     # Program start from here
    try:
        setup()
        writeLCD(0, 0, 'MENU TEST')
        time.sleep(2)
        LCD1602.clear()
        
        TestKeyPad.startReadKeys()
        
        done = False
        selectMenu = 0
        
        while (not done):
            selection = RunOptions(MENU_NAMES[selectedMenu], MENUS[selectedMenu], TestKeyPad)
            
            if (selection >= 0):
                print("Top Selection: ", TEST_OPTIONS1[selection])
                if (selection is 0):
                    selection = RunOptions("Options", TEST_OPTIONS2, TestKeyPad)
                    
            elif (selection is -1):
                print("Selection ERROR!")
                done = True
            elif (selection is -2):
                print("User Cancelled Top Menu")
                done = True
            
        TestKeyPad.stopReadKeys()
        destroy()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, end program.
        TestKeyPad.stopReadKeys()
        destroy()