import time
import KeypadPuP as KP
import HwSim as HW


if (HW.RASPI):
    import LCD1602

"""
Possible Options:

1. Set Master PW
2. Setup RFID card
3. Arm/Disarm System
"""

SelectChar = 'A' # TODO: make const
BackChar = 'B'
NextChar = 'C'
PrevChar = 'D'

MENU_RUN_SELECTION_ERROR = -1
MENU_RUN_CANCELLED = -2

class MenuData(object):

    def __init__(self, name, options, parent = ""):
        try:
            self.__parent = parent
            self.__name = name
            self.__options = options

        except:
            print("ERROR: MenuData init() error!")

    def getName(self):
        return self.__name
    
    def getParent(self):
        return self.__parent

    # Shows the options on the LCD and captures selections.
    # Returns index if the user selected valid option
    # Returns -1 if options are invalid
    # Returns -2 if user quits without selecting option
    #
    # Assumes the keyPad has started capturing
    def run(self, keyPad):
        
        retVal = -1
        index = 0
        done = False
        optCount = len(self.__options)
        if (optCount == 0):
            print("ERROR: RunOptions() - invalid options arg")
        else:
        
            increment = 0
            
            while (not done):
            #for entry in options:
                if (index >= len(self.__options)):
                    # reset to 1st option
                    index = 0
                    
                if (index < 0):
                    # reset to 1st option
                    index = len(self.__options) - 1
                    
                entry = self.__options[index]
                    
                HW.writeLCD(0, 0, self.__name)
                msg = "{}. ".format(index+1) + entry
                
                HW.writeLCD(0, 1, msg)
                
                # wait for user input
                key = keyPad.NULL
                while (key == keyPad.NULL):
                    key = keyPad.getKey()
                    
                    if (key != keyPad.NULL):
                        print("KeyPad Char Entered: ", key)
                    
                        if (key == SelectChar):
                            # capture our selection
                            retVal = index
                            done = True
                            break
                        elif (key == NextChar):
                            # go to next option
                            increment = 1
                            break
                        elif (key == PrevChar):
                            # go to previous option
                            increment = -1
                            break
                        elif (key == BackChar):
                            # user quits
                            retVal = -2
                            done = True
                            break
                        
                index += increment
                HW.clearLCD()

        return retVal

class Manager(object):
    """
    Implementations details:
    Class contains a vector of vectors of MenuData objs. All the sub menus (options) will fall under
    the top menu list (into a sub-list).
    When caller adds a MenuData obj, the mgr will find the parent menu and place it in the proper sub-list.
    When the user navigates to a top/sub menu, the mgr will navigate to the next data item in sub-list.
    It's the callers responsibility to supply the parent menu name and add the menus in the correct order.
    """

    def __init__(self):
        try:
            self.__menuList = [] #???
            
        except:
            print("ERROR: Menu Manager init() error!")

    # Checks data for parent. If one exists, function places data in the proper list.
    # Else, function places data at the top level
    def addMenu(self, data):
        
        parent = data.getParent()
        
        if (parent == ""):
            self.__menuList.append(data)
        else:
            try:
                parentIndex = self.__menuList.index(parent)
            
            except:
                print("ERROR: Menu Manager addMenu() - could not find parent !", parent)
            
            pass
        
    
        
    def run(self, keypad):
        self.__menuList[0].run(keypad)
        pass

# Shows the options on the output device and captures selections.
# Returns index if the user selected valid option
# Returns MENU_RUN_SELECTION_ERROR if options are invalid
# Returns MENU_RUN_CANCELLED if user quits without selecting option
#
# Assumes the keyPad has started capturing
def RunOptions(menuTitle, options, keyPad):
    
    retVal = MENU_RUN_SELECTION_ERROR
    index = 0
    done = False
    optCount = len(options)
    if (optCount == 0):
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
                
            HW.writeLCD(0, 0, menuTitle)
            msg = "{}. ".format(index+1) + entry
            
            HW.writeLCD(0, 1, msg)
            
            # wait for user input
            key = keyPad.NULL
            while (key == keyPad.NULL):
                key = keyPad.getKey()
                
                if (key != keyPad.NULL):
                    print("KeyPad Char Entered: ", key)
                
                    if (key == SelectChar):
                        # capture our selection
                        retVal = index
                        done = True
                        break
                    elif (key == NextChar):
                        # go to next option
                        increment = 1
                        break
                    elif (key == PrevChar):
                        # go to previous option
                        increment = -1
                        break
                    elif (key == BackChar):
                        # user quits
                        retVal = MENU_RUN_CANCELLED
                        done = True
                        break
                    
            index += increment
            HW.clearLCD()

    return retVal

# ---------
# Test Code
# ---------
TestKeyPad = KP.Keypad(KP.KEYS,KP.ROW_PINS,KP.COL_PINS)

TEST_OPTIONS1 = ["Set Master PW",
                 "Setup Card",
                 "Arm System",
                 "Disarm System",
                 "Revoke PW"]

TEST_OPTIONS2 = ["Set PW1",
                 "Set PW2"]

TEST_OPTIONS3 = ["Setup Card1",
                 "Setup Card2"]

MENU_NAMES = ["Options1", "Options2", "Options3"]
MENUS = [TEST_OPTIONS1, TEST_OPTIONS2, TEST_OPTIONS3]

def setup():
    HW.init()

def destroy():
    print("--- Menu Test Terminated By User ---")
    HW.clearLCD()

def runTestMenu(keypad):
    menuMgr = Manager()
    
    menu1 = MenuData(MENU_NAMES[0], TEST_OPTIONS1)
    menu2 = MenuData(MENU_NAMES[1], TEST_OPTIONS2, MENU_NAMES[0])
    menu3 = MenuData(MENU_NAMES[2], TEST_OPTIONS3, MENU_NAMES[1])
    
    menuMgr.addMenu(menu1)
    menuMgr.addMenu(menu2)
    menuMgr.addMenu(menu3)
    
    menuMgr.run(keypad)

if __name__ == '__main__':     # Program start from here
    try:
        setup()
        HW.writeLCD(0, 0, 'MENU TEST')
        time.sleep(2)
        HW.clearLCD()
        
        TestKeyPad.startReadKeys()
        
        done = False
        selectedMenu = 0
        
        runTestMenu(TestKeyPad)
        
        """
        while (not done):
            selection = RunOptions(MENU_NAMES[selectedMenu], MENUS[selectedMenu], TestKeyPad)
            
            # DEBUG_JW - this is test driver code. Need to implement this in the Manager.
            if (selection >= 0):
                print("Top Selection: ", TEST_OPTIONS1[selection])
                if (selection == 0):
                    selection = RunOptions("Options", TEST_OPTIONS2, TestKeyPad)
                    
            elif (selection == MENU_RUN_SELECTION_ERROR):
                print("Selection ERROR!")
                done = True
            elif (selection == MENU_RUN_CANCELLED):
                print("User Cancelled Top Menu")
                done = True
        """    
        TestKeyPad.stopReadKeys()
        destroy()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, end program.
        TestKeyPad.stopReadKeys()
        destroy()
