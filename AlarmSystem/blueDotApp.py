from bluedot import BlueDot

#TheDot = BlueDot()

TOTAL_ROWS = 100
TOTAL_COLS = 150

BACKGROUND_COLOR = "blue"
ARM_BUTTON_COLOR = "green"
DISARM_BUTTON_COLOR = "red"

# Button Types
ARM_BUTTON_TYPE = 0
DISARM_BUTTON_TYPE = 1

# Button Boundaries
ARM_BUTTON_TOP_ROW = 50
ARM_BUTTON_BOTTOM_ROW = 90
ARM_BUTTON_LEFT_COL = 3
ARM_BUTTON_RIGHT_COL = 40

DISARM_BUTTON_TOP_ROW = ARM_BUTTON_TOP_ROW
DISARM_BUTTON_BOTTOM_ROW = ARM_BUTTON_BOTTOM_ROW
DISARM_BUTTON_LEFT_COL = 80
DISARM_BUTTON_RIGHT_COL = 120

def setup(blueDot, rowCount, colCount):  
    print("Setting up... rows=%d, cols=%d" % (rowCount, colCount))
    blueDot = BlueDot(cols=colCount, rows=rowCount)
    return blueDot

def detectPress(blueDot):
    blueDot.wait_for_press()
    #print("You pressed the blue dot!")
    
def armButton_Handler(pos):
    print("ARM button pressed")

def disarmButton_Handler(pos):
    print("DISARM button pressed")
    
def background_Handler(pos):
    print("Background pressed")
    
def getButtonType(col, row):
    retType = -1
    
    if ((row > ARM_BUTTON_TOP_ROW) and (row < ARM_BUTTON_BOTTOM_ROW) and ((col > ARM_BUTTON_LEFT_COL) and (col < ARM_BUTTON_RIGHT_COL))):
        retType = ARM_BUTTON_TYPE
    elif ((row > DISARM_BUTTON_TOP_ROW) and (row < DISARM_BUTTON_BOTTOM_ROW) and ((col > DISARM_BUTTON_LEFT_COL) and (col < DISARM_BUTTON_RIGHT_COL))):
        retType = DISARM_BUTTON_TYPE
    
    return retType
    
def setupDot(blueDot, col, row):

    buttonType = getButtonType(col, row)
    
    if (buttonType == ARM_BUTTON_TYPE):
        blueDot[col,row].color = ARM_BUTTON_COLOR
        blueDot[col,row].when_pressed = armButton_Handler
    elif (buttonType == DISARM_BUTTON_TYPE):
        blueDot[col,row].color = DISARM_BUTTON_COLOR
        blueDot[col,row].when_pressed = disarmButton_Handler
    else:
        # default to background dot
        blueDot[col,row].color = BACKGROUND_COLOR
        blueDot[col,row].when_pressed = background_Handler
        
    

def cleanup(bluetoothServer):
    print("\nGoodbye!")
    #bluetoothServer.disconnect_client()


if __name__ == '__main__':     # Program start from here
    bluetoothServer = None
    
    try:
        print("Setting up... rows=%d, cols=%d" % (TOTAL_ROWS, TOTAL_COLS))
        
        blueDot = BlueDot(cols=TOTAL_COLS, rows=TOTAL_ROWS)

        for row in range(0, TOTAL_ROWS):
            for col in range(0, TOTAL_COLS):
                setupDot(blueDot, col,row)
       
        while (1):
            detectPress(blueDot)
        
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the program destroy() will be  executed.
        cleanup(bluetoothServer)