import sys, os.path

import sharedConst as Const

# --------------
# Public Methods
# --------------
def getIrCode(irCodeName):
    retCode = None
    print(irCodeName)
    
    maxRange = len(Const.IR_CODE_NAMES)
        
    for i in range(0, maxRange):

        tmpName = Const.IR_CODE_NAMES[i]

        if (tmpName == irCodeName):
            retCode = Const.IR_CODE_LOOKUP[i]
            break
    
    #DEBUG_JW
    #retCode = Const.IR_CODE_LOOKUP[Const.RemoteCmd.PLAY_PAUSE]
    return retCode


def writeIrCode(irCode):
    if (os.path.exists(Const.IR_SIM_CODE_FILE)):
        # file exists
        os.remove(Const.IR_SIM_CODE_FILE)
    
    sharedFile = open(Const.IR_SIM_CODE_FILE, "w")
    sharedFile.write(str(irCode))
    sharedFile.close()



if __name__ == "__main__":
    
    numArgs = len(sys.argv)
    print ('Number of arguments:', numArgs, 'arguments.')
    print ('Argument List:', str(sys.argv))
    
    if (numArgs < 2):
        print("ERROR: Invalid arg!")
    else:
        args = sys.argv[1:]          
        irCode = getIrCode(args[0])
        
        if (irCode == None):
            print("ERROR: No IR code match for ", args[0])
        else:
            print("IR Code Match: ")
            print(hex(irCode))
            writeIrCode(irCode)
