RASPI = False

if (RASPI):
    import LCD1602


#-------------------
# Keypad Simulation
#-------------------
__SimKeys = []
if (not RASPI):
    # <Insert Desired Keypad Simulation Sequence Here or Use Accessors To Set Keys>
    __SimKeys = ['A', 'A'] # menu test: pass
    #__SimKeys = ['A', 'C', 'A'] # menu test: pass
    #__SimKeys = ['A', 'B'] # menu test: fail
    #__SimKeys = ['B'] # menu test: pass
    #__SimKeys = ['B', 'A'] # menu test: pass
    #__SimKeys = ['C', 'A', 'A'] # menu test: fail

def GetSimKeys():
    global __SimKeys
    return __SimKeys

def SetSimKeys(keys):
    if (RASPI):
        print("ERROR: Cannot SetSimKeys when HW is enabled")
    else:
        global __SimKeys
        __SimKeys = keys
    

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

def init():
    initLCD()
    
    
if __name__ == '__main__':     # Program start from here
    print("Test Not Implemented for Simulation")