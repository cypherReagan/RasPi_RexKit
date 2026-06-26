from enum import Enum
import time
import os
import KeypadPuP as KP
import HwSim as HW


if (HW.RASPI):
    import LCD1602

# Driver Menu Actions
class Action(Enum):
    INVALID = 0
    SETPW = 1
    RFID = 2
    ARM_SYSTEM = 3
    DISARM_SYSTEM = 4

"""
Possible Options:

1. Set Master PW
2. Setup RFID card
3. Arm/Disarm System
"""

UNIT_TEST = True # Toggle For Unit Tests 
if (HW.RASPI):
    # cannot unit test on real HW
    UNIT_TEST = False
    

SELECT_CHAR = 'A' # TODO: make const
BACK_CHAR = 'B'
NEXT_CHAR = 'C'
PREV_CHAR = 'D'

# Menu Run State
MENU_RUN_SELECTION_ERROR = -1
MENU_RUN_CANCELLED = -2

# Menu Data Level State
MENU_STATE_MIDDLE_LEVEL = 0
MENU_STATE_TOP_LEVEL = 1
MENU_STATE_BOTTOM_LEVEL = 2

class MenuData(object):

    def __init__(self, name, options, parent=None, levelState=MENU_STATE_MIDDLE_LEVEL, trigger=None):
        try:
            self.__parentRef = None if isinstance(parent, str) else parent  # Object reference to parent MenuData
            self.__parentName = parent if isinstance(parent, str) else ""   # For lookup during tree building
            self.__trigger = trigger
            self.__name = name
            self.__options = options
            self.__levelState = levelState
            self.__childrenByTrigger = {}  # Maps trigger text to child MenuData objects

        except:
            print("ERROR: MenuData init() error!")

    def getName(self):
        return self.__name
    
    def getParent(self):
        """Returns the parent MenuData object"""
        return self.__parentRef
    
    def getParentName(self):
        """Returns the parent name string (used during tree building)"""
        return self.__parentName
    
    def getTrigger(self):
        return self.__trigger
    
    def getOptions(self):
        return self.__options
    
    def getOption(self, index):
        retVal = ""
        
        if (index < len(self.__options)):
            retVal = self.__options[index]
        
        return retVal

    def getLevel(self):
        return self.__levelState

    def isTopLevel(self):
        retVal = False
        if (self.__levelState == MENU_STATE_TOP_LEVEL):
            retVal = True
            
        return retVal

    def isBottomLevel(self):
        retVal = False
        if (self.__levelState == MENU_STATE_BOTTOM_LEVEL):
            retVal = True
            
        return retVal
    
    def addChild(self, childMenu, trigger):
        """Add a child menu that is triggered by a specific option"""
        self.__childrenByTrigger[trigger] = childMenu
        childMenu.__setParentRef(self)
    
    def getChild(self, trigger):
        """Get child menu by trigger text, returns None if not found"""
        return self.__childrenByTrigger.get(trigger, None)
    
    def __setParentRef(self, parentRef):
        """Internal method to set the parent object reference"""
        self.__parentRef = parentRef

    # Class: MenuData
    # Shows the options on the LCD and captures selections.
    # Returns index if the user selected valid option
    # Returns MENU_RUN_SELECTION_ERROR if options are invalid
    # Returns MENU_RUN_CANCELLED if user quits without selecting option
    #
    # Assumes the keyPad has started capturing
    def run(self, keyPad):
        
        retVal = MENU_RUN_SELECTION_ERROR
        index = 0
        done = False
        optCount = len(self.__options)
        if (optCount == 0):
            print("ERROR: MenuData.run() - invalid options arg")
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
                    
                        if (key == SELECT_CHAR):
                            # capture our selection
                            retVal = index
                            done = True
                            break
                        elif (key == NEXT_CHAR ):
                            # go to next option
                            increment = 1
                            break
                        elif (key == PREV_CHAR):
                            # go to previous option
                            increment = -1
                            break
                        elif (key == BACK_CHAR):
                            # user quits
                            retVal = MENU_RUN_CANCELLED
                            done = True
                            break
                        
                index += increment
                HW.clearLCD()

        return retVal

class Manager(object):
    """
    Menu tree manager using object references for parent-child relationships.
    
    Implementation details:
    - Stores top-level menus in __topLevelMenus
    - Child menus are stored as object references in their parent MenuData
    - No string-based lookups; navigation uses direct object references
    - Supports backward compatibility with string-based parent names during menu addition
    """

    def __init__(self):
        try:
            self.__topLevelMenus = []  # Only top-level menus
            self.__allMenusByName = {}  # Name to MenuData mapping for tree building
            
        except:
            print("ERROR: Menu Manager init() error!")

    def __findMenuByName(self, name):
        """Find a menu by its unique name (used during tree building)"""
        return self.__allMenusByName.get(name, None)
        
    def addMenu(self, data):
        """
        Add a menu to the tree structure.
        
        If parent is a string name, finds the parent object and establishes the relationship.
        If parent is "", adds as a top-level menu.
        If parent is a MenuData object, adds as a child directly.
        """
        
        # Register this menu by name for lookup
        self.__allMenusByName[data.getName()] = data
        
        parentName = data.getParentName()
        
        if parentName == "":
            # Top-level menu
            self.__topLevelMenus.append(data)
        else:
            # Child menu - find parent by name and establish relationship
            parentMenu = self.__findMenuByName(parentName)
            
            if parentMenu is not None:
                trigger = data.getTrigger()
                if trigger is not None:
                    parentMenu.addChild(data, trigger)
                else:
                    print("ERROR: Menu Manager addMenu() - child menu missing trigger: ", data.getName())
            else:
                print("ERROR: Menu Manager addMenu() - could not find parent menu: ", parentName)
        
    def run(self, keypad):
        """
        Run the menu system and return the final selection.
        Uses object references to navigate the menu tree.
        """
        
        retName = ""
        done = False
        currentMenu = self.__topLevelMenus[0] if len(self.__topLevelMenus) > 0 else None
        
        try:
            while (not done) and currentMenu is not None:
                selection = currentMenu.run(keypad)
                
                if (selection == MENU_RUN_SELECTION_ERROR):
                    print("ERROR: Menu Manager run() - invalid selection")
                    done = True
                    break
                elif (selection == MENU_RUN_CANCELLED):
                    if (currentMenu.isTopLevel()):
                        done = True
                        break
                    # Navigate back to parent using object reference
                    currentMenu = currentMenu.getParent()
                    if currentMenu is None:
                        currentMenu = self.__topLevelMenus[0] if len(self.__topLevelMenus) > 0 else None
                        if currentMenu is None:
                            print("ERROR: Menu Manager run() - could not find parent menu")
                            done = True
                    continue
                
                selectedOption = currentMenu.getOption(selection)
                # Get child menu using object reference instead of string lookup
                childMenu = currentMenu.getChild(selectedOption)
                
                if childMenu is not None:
                    currentMenu = childMenu
                    continue
                
                # No child menu; return current selection as final action.
                retName = selectedOption
                done = True
        except Exception as e:
            print("ERROR: Menu Manager run() - Exception Occurred: ", e)
        
        return retName
    
# ---------
# Test Code
# ---------
TestKeyPad = KP.Keypad(KP.KEYS_ALL,KP.ROW_PINS,KP.COL_PINS)

TEST_OPTIONS1 = ["Set Master PW",
                 "Setup Card",
                 "Arm System",
                 "Disarm System",
                 "Revoke PW"]

TEST_OPTIONS2 = ["Set PW1",
                 "Set PW2"]

TEST_OPTIONS3 = ["Setup Card1",
                 "Setup Card2"]

MENU_NAMES = ["OptionsLevel1", "OptionsLevel2", "OptionsLevel3"]
MENUS = [TEST_OPTIONS1, TEST_OPTIONS2, TEST_OPTIONS3]

Password1 = ""
Password2 = ""

MenuMgr = None
MenuLookup = []

def setup():
    HW.init()
    HW.SetSimKeys([])
    
    # clear colsole for new run
    for i in range(20):
        print(i)
        clearConsole()
    
    # init menu data
    global MenuMgr
    MenuMgr = Manager()
    
    #               "Options1"      ["Set Master PW","Setup Card"...]  parent=""                 TopLevel
    menu1 = MenuData(MENU_NAMES[0], TEST_OPTIONS1,                     "",                       MENU_STATE_TOP_LEVEL)
    #               "Options2"      ["Set PW1","Set PW2"]              parent="OptionsLevel1"    BottomLevel
    menu2 = MenuData(MENU_NAMES[1], TEST_OPTIONS2,                     MENU_NAMES[0],            MENU_STATE_BOTTOM_LEVEL, trigger = TEST_OPTIONS1[0])
    #               "Options3"      ["Setup Card1","Setup Card2"]      parent="OptionsLevel1"    BottomLevel
    menu3 = MenuData(MENU_NAMES[2], TEST_OPTIONS3,                     MENU_NAMES[0],            MENU_STATE_BOTTOM_LEVEL, trigger = TEST_OPTIONS1[1])
    
    MenuMgr.addMenu(menu1)
    MenuMgr.addMenu(menu2)
    MenuMgr.addMenu(menu3)
    
    global MenuLookup
    MenuLookup = {
            TEST_OPTIONS2[0]: SetPw1,
            TEST_OPTIONS2[1]: SetPw2,
            TEST_OPTIONS3[0]: SetupCard1,
            TEST_OPTIONS3[1]: SetupCard2,
        }

def SetPw1(keypad):
    if (not UNIT_TEST):
        global Password1
        Password1 = input('Enter Password1 in console: ')
    
def SetPw2(keypad):
    if (not UNIT_TEST):
        global Password2
        Password2 = input('Enter Password2 in console: ')

def SetupCard1(keypad):
    print("Setup Card1 complete")
    
def SetupCard2(keypad):
    print("Setup Card2 complete")

def destroy():
    print("--- Menu Test Terminated By User ---")
    HW.clearLCD()
    
def clearConsole():
    print("\n"*47)

def runUnitTest(keypad, testNum, keys, expectedMenu):
    HW.SetSimKeys(keys)
    menu = runMenuTest(keypad)

    testResult = "FAIL"    
    if (menu == expectedMenu):
        testResult = "PASS" 
        
    printTestResult(testNum, testResult)
    pass

def unitTestRunner(keypad):
    global MenuMgr
    global MenuLookup
    
    if (not HW.RASPI): 
        # ----------
        # Test 1
        # ----------
        testNum = 1
        """Unit Test: Select "Set Master PW" then "Set PW1" from the menu"""
        runUnitTest(keypad, testNum, [SELECT_CHAR, SELECT_CHAR], TEST_OPTIONS2[0])
    
        # ----------
        # Test 2
        # ----------
        testNum += 1
        """Unit Test: Select "Set Master PW" then "Set PW2" from the menu"""
        runUnitTest(keypad, testNum, [SELECT_CHAR, NEXT_CHAR, SELECT_CHAR], TEST_OPTIONS2[1])
    
        # ----------
        # Test 3
        # ----------
        testNum += 1
        """Unit Test: Select "Setup Card" then "Setup Card1" from the menu"""
        runUnitTest(keypad, testNum, [NEXT_CHAR, SELECT_CHAR, SELECT_CHAR], TEST_OPTIONS3[0])

        # ----------
        # Test 4
        # ----------
        testNum += 1
        """Unit Test: Select "Setup Card" (with backward navigation)then "Setup Card1" from the menu"""
        runUnitTest(keypad, testNum, [NEXT_CHAR, NEXT_CHAR, BACK_CHAR, SELECT_CHAR, SELECT_CHAR], TEST_OPTIONS3[0])
    
    
def runMenuTest(keypad):
    global MenuMgr
    global MenuLookup
    
    menu = MenuMgr.run(keypad)

    if (menu == ""):
        print("ERROR: invalid menu returned from test run")
    else:
        print("Test run returned menu:  ", menu)
        MenuLookup[menu](keypad)

        print("Password1 = ", Password1)
        print("Password2 = ", Password2)
        
    return menu

def printTestResult(testNum, testResult):
    print("---------------------------------")
    print("Test ", testNum, " : ",testResult)
    print("---------------------------------")
    
if __name__ == '__main__':     # Program start from here
    try:
        setup()
        HW.writeLCD(0, 0, 'MENU TEST')
        time.sleep(2)
        HW.clearLCD()
        
        TestKeyPad.startReadKeys()

        if (UNIT_TEST):
            unitTestRunner(TestKeyPad) # unit tests with simKeys
        else:
            runMenuTest(TestKeyPad) 
 
        TestKeyPad.stopReadKeys()
        destroy()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, end program.
        TestKeyPad.stopReadKeys()
        destroy()