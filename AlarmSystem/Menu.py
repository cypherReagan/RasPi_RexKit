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
    

SelectChar = 'A' # TODO: make const
BackChar = 'B'
NextChar = 'C'
PrevChar = 'D'

# Menu Run State
MENU_RUN_SELECTION_ERROR = -1
MENU_RUN_CANCELLED = -2

# Menu Data Level State
MENU_STATE_MIDDLE_LEVEL = 0
MENU_STATE_TOP_LEVEL = 1
MENU_STATE_BOTTOM_LEVEL = 2

class MenuData(object):

    def __init__(self, name, options, parent, levelState = MENU_STATE_MIDDLE_LEVEL, trigger = None):
        try:
            self.__parent = parent
            self.__trigger = trigger
            self.__name = name
            self.__options = options
            self.__levelState = levelState

        except:
            print("ERROR: MenuData init() error!")

    def getName(self):
        return self.__name
    
    def getParent(self):
        return self.__parent
    
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
            self.__selected = 0
            
        except:
            print("ERROR: Menu Manager init() error!")

    # Class: Manager
    # Find the parent index from the given name
    # Return index is valid index if name match found, else -1
    def __findParentIndex(self, name):
        retIndex = -1
        
        maxLen = len(self.__menuList)
        
        for index in range(maxLen):
            if (name == self.__menuList[index].getName()):
                retIndex = index
                break
        
        return retIndex

    # Class: Manager
    # Find the child options index from the given parent name
    # Return index is valid index if options found, else -1
    def __findOptionsIndexFromParent(self, parentName):
        retIndex = -1
        maxLen = len(self.__menuList)
        
        for index in range(0, maxLen):
            if (parentName == self.__menuList[index].getParent()):
                retIndex = index
                break
            
        return retIndex
    
    # Class: Manager
    # Find the child menu for the given parent menu name and selected option label
    # Return the matching MenuData object, else None
    def __findChildMenuByOption(self, parentMenuName, selectedOption):
        for menu in self.__menuList:
            if menu.getParent() == parentMenuName and menu.getTrigger() == selectedOption:
                return menu
        return None
    
    # Class: Manager
    # Find a menu by its unique name
    def __findMenuByName(self, name):
        for menu in self.__menuList:
            if menu.getName() == name:
                return menu
        return None
    
    # Class: Manager
    # Find the child options from the given parent name
    # Return list is valid if options found, else empty
    def __getChildOptionsFromParent(self, parentName):
        retChildOptions = []
        
        childOptionsIndex = self.__findOptionsIndexFromParent(parentName)
        
        if (childOptionsIndex == -1):
            print("ERROR: Menu Manager getChildOptionsFromParent() - could not find childOptions index for parentName: ", parentName)
        else:
            retChildOptions = self.__menuList[childOptionsIndex].getOptions()

        return retChildOptions
        
    # Class: Manager
    # Checks data for parent. If one exists, function places data in the proper list.
    # Else, function places data at the top level
    def addMenu(self, data):
        
        parent = data.getParent()
        
        if (parent == ""):
            self.__menuList.append(data)
        else:
            parentIndex = -1
            try:
                #parentIndex = self.__menuList.index(parent)
                parentIndex = self.__findParentIndex(parent)
            
            except:
                print("ERROR: Menu Manager addMenu() - could not find parent ", parent)
            
            if (parentIndex != -1):
                 self.__menuList.insert(parentIndex+1, data)
            else:
                print("ERROR: Menu Manager addMenu() - could not find parent ", parent)
                
            pass
        
    # Class: Manager
    # Shows the options on the output device and captures selections.
    # Returns name of the menu selected, else empty string
    #
    # Assumes the keyPad has started capturing
    def run(self, keypad):
        
        retName = ""
        done = False
        currentMenu = self.__menuList[0] if len(self.__menuList) > 0 else None
        
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
                    currentMenu = self.__findMenuByName(currentMenu.getParent())
                    if currentMenu is None:
                        currentMenu = self.__menuList[0] if len(self.__menuList) > 0 else None
                        if currentMenu is None:
                            print("ERROR: Menu Manager run() - could not find parent menu")
                            done = True
                    continue
                
                selectedOption = currentMenu.getOption(selection)
                childMenu = self.__findChildMenuByOption(currentMenu.getName(), selectedOption)
                
                if childMenu is not None:
                    currentMenu = childMenu
                    continue
                
                # No child menu; return current selection as final action.
                retName = selectedOption
                done = True
        except Exception as e:
            print("ERROR: Menu Manager run() - Exception Occurred: ", e)
        
        return retName
            
    # Class: Manager
    # Generates a new menu based on the child options of the given selection
    def __generateMenuFromChildOptions(self, selMenuList, menuIndex, childOptionsIndex):
        
        retList = []
        
        if (childOptionsIndex >= len(selMenuList)):
            print("ERROR: Menu Manager generateMenuFromChildOptions() - Invalid childOptionsIndex =", childOptionsIndex, " when listSize =", len(selMenuList))
        else:
            # NOTE: each new menu item will have the duplicate options if we're are the bottom level
            level = selMenuList[childOptionsIndex].getLevel()
            childName = selMenuList[childOptionsIndex].getName()
            childOptions = selMenuList[childOptionsIndex].getOptions()
            parentName = selMenuList[menuIndex].getName()

            for item in childOptions:
                newChildOptions = self.__getChildOptionsFromParent(parentName) 
                menu = MenuData(childName, newChildOptions, parentName, level)
                retList.append(menu)
    
        return retList
    
    # Class: Manager
    # Generates a new menu based on the parent options of the given selection
    def __generateMenuFromParentOptions(self, selMenuList, menuIndex, childOptionsIndex):
        
        retList = []
        
        # NOTE: each new menu item will have the duplicate options if we're are the bottom level
        level = selMenuList[childOptionsIndex].getLevel()
        childName = selMenuList[childOptionsIndex].getName()
        childOptions = selMenuList[childOptionsIndex].getOptions()
        parentName = selMenuList[menuIndex].getName()

        for item in childOptions:
            newChildOptions = self.__getChildOptionsFromParent(parentName) 
            menu = MenuData(childName, newChildOptions, parentName, level)
            retList.append(menu)
    
        return retList
    
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
    
    #               "Options1"   ["Set Master PW","Setup Card"...]  ""         TopLevel
    menu1 = MenuData(MENU_NAMES[0], TEST_OPTIONS1, "", MENU_STATE_TOP_LEVEL)
    #               "Options2"   ["Set PW1","Set PW2"]           "OptionsLevel1"    BottomLevel
    menu2 = MenuData(MENU_NAMES[1], TEST_OPTIONS2, MENU_NAMES[0], MENU_STATE_BOTTOM_LEVEL, trigger = TEST_OPTIONS1[0])
    #               "Options3"   ["Setup Card1","Setup Card2"]   "OptionsLevel1"    BottomLevel
    menu3 = MenuData(MENU_NAMES[2], TEST_OPTIONS3, MENU_NAMES[0], MENU_STATE_BOTTOM_LEVEL, trigger = TEST_OPTIONS1[1])
    
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

def runMenuUnitTests(keypad):
    global MenuMgr
    global MenuLookup
    
    if (not HW.RASPI): 
        # ----------
        # Test 1
        # ----------
        testNum = 1
        keys = ['A', 'A'] # select "Set PW1"
        HW.SetSimKeys(keys)
        
        menu = runMenuTest(keypad)
            
        testResult = "FAIL"    
        if (menu == TEST_OPTIONS2[0]):
            testResult = "PASS" 
            
        printTestResult(testNum, testResult)
    
        # ----------
        # Test 2
        # ----------
        testNum += 1
        keys = ['A', 'C', 'A'] # select "Set Master PW", then "Set PW2"
        HW.SetSimKeys(keys)
        
        menu = runMenuTest(keypad)
            
        testResult = "FAIL"    
        if (menu == TEST_OPTIONS2[1]):
            testResult = "PASS" 
            
        printTestResult(testNum, testResult)
    
        # ----------
        # Test 3
        # ----------
        testNum += 1
        keys = ['B', 'A'] # select "Setup Card", then "Setup Card1"
        HW.SetSimKeys(keys)
        
        menu = runMenuTest(keypad)
            
        testResult = "FAIL"    
        if (menu == TEST_OPTIONS3[0]):
            testResult = "PASS" 
            
        printTestResult(testNum, testResult)
    
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
            runMenuUnitTests(TestKeyPad) # unit tests with simKeys
        else:
            runMenuTest(TestKeyPad) 
 
        TestKeyPad.stopReadKeys()
        destroy()
    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, end program.
        TestKeyPad.stopReadKeys()
        destroy()