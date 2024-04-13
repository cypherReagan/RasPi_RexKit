import time
import LCD1602
import KeypadPuP as KP

"""
Possible Options:

1. Set Master PW
2. Setup RFID card
3. Arm/Disarm System
"""


def DisplayOptions(menuTitle, options):
    
    count = 1
    
    for entry in options:
        writeLCD(0, 0, menuTitle)
        msg = "{}. ".format(count) + entry
        
        writeLCD(0, 1, msg)
        
        # wait for user input
        
        time.sleep(2)
        count += 1
        LCD1602.clear()

    

# ---------
# Test Code
# ---------
TEST_OPTIONS = ["Set Master PW",
                "Setup Card",
                "Arm System",
                "Disarm System"]

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
        
        DisplayOptions("Options", TEST_OPTIONS)
        
        destroy()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, end program.
        destroy()