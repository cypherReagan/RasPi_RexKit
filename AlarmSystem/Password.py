import random
import os


KEYS = ['1','2','3','A',
        '4','5','6','B',
        '7','8','9','C',
        '*','0','#','D']

class PasswordData(object):
    
    #constructor
    def __init__(self, pwLen, pwKeys, initialPW = []):
        self.password=[]
        self.passwordDict={}
        randomWord = True

        if (pwLen <= 0):
            print("ERROR: invalid PW len ",pwLen)
        else:
            if (len(initialPW) == pwLen):
                # use this for data
                for key in initialPW:
                    self.password.append(key)
                    
                randomWord = False
                print("DEBUG_JW: PasswordData() - init from given PW")
            else:
                # generate our own word
                print("DEBUG_JW: PasswordData() - init from generated PW")
                
                count = 0
                while (count < pwLen):
                    count += 1
                    self.password.append('0') # will be populated randomly
                
            self.generateWord(pwKeys, randomWord)

    # Class: PasswordData
    def generateWord(self, pwKeys, randomWord = True):
        pwLen = len(self.password)
        keysLen = len(pwKeys)-1
        
        for i in range(pwLen):
            if (randomWord):
                rand = random.randint(0, keysLen)
                self.password[i] = pwKeys[rand]
            
            print("DEBUG_JW: new pw key = ",self.password[i])
            
            # is generated key in dict?
            # if so, update keyVal with count, else add key
            count = 1
            if self.password[i] in self.passwordDict.keys():
                count = self.passwordDict[self.password[i]]
                count += 1
                print("DEBUG_JW: key already in dict, updating count")
                
            self.passwordDict.update({self.password[i]: count})
            
            print("DEBUG_JW: dict = ",self.passwordDict, "\n")
    
    
    
class Password(object):
    
    INCORRECT_CHAR = 'N'
    CORRECT_CHAR = 'Y'
    INCORRECT_PLACE_CHAR = 'I'
    
    #constructor
    def __init__(self, pwLen, pwKeys, initialPW = []):
        self.init(pwLen, pwKeys, initialPW)
        
    # Class: Password
    def init(self, pwLen, pwKeys, initialPW = []):
        self.__password=[]
        self.__data = PasswordData(pwLen, pwKeys, initialPW)
        
    # Class: Password
    def printWord(self):
        print("PW:\t", self.__data.password)
        
    # Class: Password
    def getString(self):
        delimiter = "" # Define a delimiter
        pwStr = delimiter.join(self.__data.password)
        return pwStr
        
    # Class: Password    
    def checkWholeWord(self, word):
        for i in range(0,len(self.__data.password)):
            if(self.__data.password[i]!=word[i]):
                return 0
        return 1
    
    # Class: Password
    def isCharInWord(self, char):
        for i in range(0,len(self.__data.password)):
            if(self.__data.password[i]== char):
                return True
        return False
    
    # Class: Password
    def isCharInWord_NEW(self, char, pos, wordDict):
        for i in range(0,len(self.__data.password)):
            if(self.__data.password[i]== char):
                return True
        return False
    
    # Class: Password
    def getCompareResult(self, word):
        result = []
        
        if (len(self.__data.password) != len(word)):
            print("ERROR: invalid compare PW len ",len(word))
        else:
        
            for i in range(0, len(self.__data.password)):
                
                
                
                if (self.__data.password[i] == word[i]):
                    result.append(self.CORRECT_CHAR)
                elif (self.isCharInWord(word[i])):
                    result.append(self.INCORRECT_PLACE_CHAR)         
                else:
                    result.append(self.INCORRECT_CHAR)
        
        return result
    
    # Class: Password
    def saveToDisk(self, fileName):

        with open(fileName, "w", encoding="utf-8") as file:
            file.write(self.getString())
            file.close()
            
    # Class: Password
    def readFromDisk(self, fileName):

        with open(fileName, "r", encoding="utf-8") as file:
            pwStr = file.read()
            print("readFromDisk: " + pwStr)
            file.close()
            # now update our PasswordData
            pwList = list(pwStr)
            self.init(len(pwList), KEYS, pwList)# DEBUG_JW - TODO: don't hardcode KEYS here
            


# Static Methods
def IsCorrectResult(word):
    
    retVal = True
    
    for i in range(0, len(word)):
         if (word[i] != Password.CORRECT_CHAR):
             retVal = False
             break

    return retVal

# ---------
# Test Code
# ---------
PW_TEST_FILE = "PwTestFile.txt"

def destroy():
    print("Cleanup here...")
    
def guessPW(testPW, testWord):
    print("Guess:\t", testWord)
    result = testPW.getCompareResult(testWord)
    print("Result:\t", result)
    print("\n")


def PwGuessTest():
    # generated PW test
    print("--- RANDOMLY GENERATED PASSWORD---")
    testPwGen = Password(TEST_PW_LEN, KEYS)
    testPwGen.printWord()
    print("\n")
    

    guessPW(testPwGen, ['0','0','0','0'])
    guessPW(testPwGen, ['1','1','1','1'])
    guessPW(testPwGen, ['2','2','2','2'])
    guessPW(testPwGen, ['1','2','3','4'])
    guessPW(testPwGen, ['A','#','B','C'])
    
    #non-generated PW test
    print("--- SUPPLIED MASTER PASSWORD---")
    masterPW = ['1','2','3','4']
    testPw = Password(TEST_PW_LEN, KEYS, masterPW)
    testPw.printWord()
    print("\n")

    guessPW(testPw, ['0','0','0','0'])
    guessPW(testPw, ['1','1','1','1'])
    guessPW(testPw, ['2','2','2','2'])
    guessPW(testPw, ['1','2','3','4'])
    guessPW(testPw, ['A','#','B','C'])

def PwWriteTest():
    file = os.path.abspath(os.getcwd()) + "/" + PW_TEST_FILE
    print("PwWriteTest: " + file)
    
    masterPW = ['1','2','3','4']
    testPW = Password(len(masterPW), KEYS, masterPW)
    testPW.saveToDisk(file)
    
def PwReadTest():
    file = os.path.abspath(os.getcwd()) + "/" + PW_TEST_FILE
    print("DEBUG_JW: PwReadTest: " + file)
    
    masterPW = ['4','3','2','1']
    testPW = Password(len(masterPW), KEYS, masterPW)
    testPW.readFromDisk(file)
    testPW.printWord()

if __name__ == '__main__':     # Program start from here
    try:
        #PwGuessTest()
        PwWriteTest()
        PwReadTest()

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, cleanup.
        destroy()