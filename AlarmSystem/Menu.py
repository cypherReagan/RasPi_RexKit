import time
import os
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

UNIT_TEST = False
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

    def __init__(self, name, options, parent, levelState = MENU_STATE_MIDDLE_LEVEL):
        try:
            self.__parent = parent
            self.__name = name
            self.__options = options
            self.__levelState = levelState

        except:
            print("ERROR: MenuData init() error!")

    def getName(self):
        return self.__name
    
    def getParent(self):
        return self.__parent
    
    def getOptions(self):
        return self.__options
    
    def getOption(self, index):
        retVal = ""
        
        if (index < len(self.__options)):
            retVal = self.__options[index]
        
        return retVal

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
        menuIndex = 0
        
        selMenuList = self.__menuList # start at top-level
        
        try:
        
            while(not done):
                
                prevIndex = menuIndex
                menuIndex = selMenuList[menuIndex].run(keypad) # fire off the current menu item and get the selection returned
                
                isValid = False
                
                if ((menuIndex < MENU_RUN_CANCELLED) or (menuIndex == MENU_RUN_SELECTION_ERROR) or (menuIndex >= len(selMenuList))):
                    print("ERROR: Menu Manager run() - invalid menuIndex from run() =  ", menuIndex, " and len(selMenuList) = ", len(selMenuList))
                    done = True
                elif (menuIndex == MENU_RUN_CANCELLED):
                    # user backs out of current level
                    # TODO: generate new menu based on the parent
                    menuIndex = prevIndex
                    if (selMenuList[menuIndex].isTopLevel()):
                        # the current level is at the top so backing out quits entire menu
                        done = True
                    else:
                        # go back a level
                        parentIndex = self.__findOptionsIndexFromParent(selMenuList[menuIndex].getParent())
                        if (index == -1):
                            print("ERROR: Could not find parent index!")
                            done = True
                        else:
                            menuIndex = parentIndex
                            isValid = True
                else:
                    # got a valid selection
                    isValid = True
                    
                if (isValid):
                    if (selMenuList[menuIndex].isBottomLevel()):
                        # found bottom-level menu so quit done here
                        retName = selMenuList[menuIndex].getOption(menuIndex)
                        done = True
                    else:
                        # generate a new MenuData list based on the options
                        parentOptions = selMenuList[menuIndex].getOptions()
                        searchName = selMenuList[menuIndex].getName()
                        childOptionsIndex = self.__findOptionsIndexFromParent(searchName) # locate the child options of the target menu
                        
                        if (childOptionsIndex == -1):
                            print("ERROR: Menu Manager run() - could not find childOptions index for parentName: ", searchName)
                        else:
                            # move down a level
                            #selMenuList = self.__generateMenuFromChildOptions(selMenuList, menuIndex, childOptionsIndex)
                            umm what????
                            menuIndex = childOptionsIndex # we've created a new list so reset index here
                            
                            if (len(selMenuList) == 0):
                                print("ERROR: Menu Manager run() - new menu list empty")
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
            isBottomLevel = selMenuList[childOptionsIndex].isBottomLevel()
            childName = selMenuList[childOptionsIndex].getName()
            childOptions = selMenuList[childOptionsIndex].getOptions()
            parentName = selMenuList[menuIndex].getName()

            for item in childOptions:
                newChildOptions = self.__getChildOptionsFromParent(parentName) 
                menu = MenuData(childName, newChildOptions, parentName, isBottomLevel)
                retList.append(menu)
    
        return retList
    
    # Class: Manager
    # Generates a new menu based on the parent options of the given selection
    def __generateMenuFromParentOptions(self, selMenuList, menuIndex, childOptionsIndex):
        
        retList = []
        
        # NOTE: each new menu item will have the duplicate options if we're are the bottom level
        isBottomLevel = selMenuList[childOptionsIndex].isBottomLevel()
        childName = selMenuList[childOptionsIndex].getName()
        childOptions = selMenuList[childOptionsIndex].getOptions()
        parentName = selMenuList[menuIndex].getName()

        for item in childOptions:
            newChildOptions = self.__getChildOptionsFromParent(parentName) 
            menu = MenuData(childName, newChildOptions, parentName, isBottomLevel)
            retList.append(menu)
    
        return retList
    
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

Password1 = ""
Password2 = ""

MenuMgr = None
MenuLookup = []

def setup():
    HW.init()
    
    # clear colsole for new run
    for i in range(20):
        print(i)
        clearConsole()
    
    # init menu data
    global MenuMgr
    MenuMgr = Manager()
    
    #               "Options1"   ["Set Master PW","Setup Card"...]  ""         TopLevel
    menu1 = MenuData(MENU_NAMES[0], TEST_OPTIONS1, "", MENU_STATE_TOP_LEVEL)
    #               "Options2"   ["Set PW1","Set PW2"]           "Options1"    BottomLevel
    menu2 = MenuData(MENU_NAMES[1], TEST_OPTIONS2, MENU_NAMES[0], MENU_STATE_BOTTOM_LEVEL)
    #               "Options3"   ["Setup Card1","Setup Card2"]   "Options2"    BottomLevel
    menu3 = MenuData(MENU_NAMES[2], TEST_OPTIONS3, MENU_NAMES[1], MENU_STATE_BOTTOM_LEVEL)
    
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
    printf("Setup Card1 complete")
    
def SetupCard2(keypad):
    printf("Setup Card2 complete")

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
        keys = ['B', 'A', 'C', 'A'] # back up level and select "Set PW2"
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
        keys = ['B', 'C', 'A'] # back up level and select "Setup Card1"
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