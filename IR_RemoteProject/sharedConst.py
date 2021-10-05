from enum import Enum
from enum import IntEnum

# Globals
SIMULATE_IR_CODE = True

# Shared Files
IR_SIM_CODE_FILE_PATH = "/home/pi/Documents/Code/RexKit/JW_Code/IR_RemoteProject/IrSimCodes"
IR_SIM_CODE_FILE = IR_SIM_CODE_FILE_PATH + "/irCode.txt"

# IR Codes
#                 POWER      MODE      MUTE     PLAY       REWIND    FOWARD    EQ        MINUS    PLUS      REDO       ZERO     ONE        TWO     THREE      FOUR      FIVE      SIX       SEVEN     EIGHT     NINE      USBSCAN
IR_CODE_LOOKUP = [0xffa25d, 0xff629d, 0xffe21d, 0xff22dd, 0xff02fd, 0xffc23d, 0xffe01f, 0xffa857, 0xff906f, 0xff9867, 0xff6897, 0xff30cf, 0xff18e7, 0xff7a85, 0xff10ef, 0xff38c7, 0xff5aa5, 0xff42bd, 0xff4ab5, 0xff52ad, 0xffb04f]
IR_CODE_NAMES  = ["POWER",  "MODE",    "MUTE",  "PLAY",   "REWIND", "FOWARD", "EQ",     "MINUS",  "PLUS",   "REDO",   "ZERO",   "ONE",    "TWO",    "THREE",  "FOUR",   "FIVE",   "SIX",    "SEVEN",  "EIGHT",  "NINE",   "USBSCAN"]


class RemoteCmd(IntEnum):
    POWER = 0
    MODE = 1
    MUTE = 2
    PLAY_PAUSE = 3
    REWIND = 4
    FASTFOWARD = 5
    EQ = 6
    MINUS = 7
    PLUS = 8
    REDO = 9
    ZERO = 10
    ONE = 11
    TWO = 12
    THREE = 13
    FOUR = 14
    FIVE = 15
    SIX = 16
    SEVEN = 17
    EIGHT = 18
    NINE = 19
    USBSCAN = 20
    
