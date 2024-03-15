import RPi.GPIO as GPIO
from enum import Enum


#https://www.theengineeringprojects.com/2023/01/interface-rfid-module-rc522-with-raspberry-pi-4.html

from mfrc522 import SimpleMFRC522

class Operation(Enum):
    READ = 1
    WRITE = 2

TheReader = None

class Reader(object):
    
    def __init__(self):
        self.__theReader = None
        self.__initReader()
        
    def __initReader(self):
        self.__theReader = SimpleMFRC522()
        
        if (self.__theReader == None):
            # should not get here
            print("ERROR: Could not init MFRC522 reader!")
            
    # Returns tag id, text        
    def read(self):
        id, text = self.__theReader.read()
        return id, text
    
    def write(self, text):
        self.__theReader.write(text)




################ SIMPLE RFID TEST ################
def getUserOpInput():
    
    retVal = 0
    
    try:
        print("Available operations:\n READ = %d\n WRITE = %d" % (Operation.READ.value, Operation.WRITE.value))
        text = input('OP:')
        
        retVal = int(text)
    except ValueError:
        print("ERROR: Invalid number to be converted. ")
        retVal = 0
    
    return retVal

def WriteTag(reader):
    text = input('New data:')
    print("Now place your tag to write")
    reader.write(text)
    print("Written")

def ReadTag(reader):
    print("Now place your tag to read")
    id, text = reader.read()
    print(id)
    print(text)
    
def TestRfidOps(reader):
    try:
            
        op = getUserOpInput()
        
        if (op == Operation.READ.value):
            ReadTag(reader)
        elif (op == Operation.WRITE.value):
            WriteTag(reader)
        else:
            print("ERROR: RFID.TestRfidOps() - Invalid tag operation")

    finally:
        GPIO.cleanup()


if __name__ == '__main__':     # Program start from here
    TheReader = Reader()
    TestRfidOps(TheReader)
    