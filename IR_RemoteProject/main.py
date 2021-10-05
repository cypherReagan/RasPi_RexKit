import time, os
from enum import Enum

import LCD1602
import irRecv
import sharedConst as Const
    

def getSimIrCode():
    #print("Start getSimIrCode()")
    retCode = None
    
    done = False
    
    while (done != True):
        time.sleep(3)
        
        if (os.path.exists(Const.IR_SIM_CODE_FILE)):
            # file exists
            sharedFile = open(Const.IR_SIM_CODE_FILE,'r')
            try:
                fileTxt = sharedFile.read()
                print("Received simulated code: ", fileTxt)
                retCode = int(fileTxt)
                done = True
            finally:
                sharedFile.close()
                os.remove(Const.IR_SIM_CODE_FILE)
            
            #retCode = Const.IR_CODE_LOOKUP[Const.RemoteCmd.PLAY_PAUSE] # DEBUG_JW - for testing
    
    return retCode

def getIrCodeIndex(irCode):
    retIndex = None
    
    if 1:
    
        maxRange = len(Const.IR_CODE_LOOKUP)
        
        for i in range(0, maxRange):
            tmpVal = Const.IR_CODE_LOOKUP[i]
            #print(tmpVal)
            if (tmpVal == irCode):
                retIndex = i
                #print("DEBUG_JW: getIrCodeIndex() - found match at index ", i)
                break
    
    return retIndex

def handleIrCode(irCode):
    if irCode:
        print("------ Code Details ------")
        #print(str(irCode))
        print(str(hex(irCode)))
        print(str(bin(irCode)))
        
        irCodeIndex = getIrCodeIndex(irCode)
        if irCodeIndex:
            print("Cmd: ", Const.IR_CODE_NAMES[irCodeIndex])
        else:
            print("ERROR: IR code NOT in table")
            
        print("--------------------------")
    else:
        print("ERROR: Invalid IR code")




# Main
if __name__ == "__main__":
    
    irRecv.setup()
    
    try:
        print("Starting IR Listener")
        while True:
            print("Waiting for signal")
            
            if (Const.SIMULATE_IR_CODE):
                irCode = getSimIrCode()
            else:
                irCode = irRecv.getIrCode()
                
            handleIrCode(irCode)

                
    except KeyboardInterrupt:
        # User pressed CTRL-C
        # Reset GPIO settings
        print("Ctrl-C pressed!")
    except RuntimeError:
        # this gets thrown when control C gets pressed
        # because wait_for_edge doesn't properly pass this on
        pass
    print("Quitting")
    irRecv.destroy()
