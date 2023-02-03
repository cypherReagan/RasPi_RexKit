import random


KEYS = ['1','2','3','A',
        '4','5','6','B',
        '7','8','9','C',
        '*','0','#','D']

TEST_PW_LEN = 4

class PasswordData(object):
    
    #constructor
    def __init__(self, pwLen, pwKeys):
        self.password=[]
        self.passwordDict={}

        if (pwLen <= 0):
            print("ERROR: invalid PW len ",pwLen)
        else:
            count = 0
            while (count < pwLen):
                count += 1
                self.password.append('0')
                
            self.generateWord(pwKeys)

    def generateWord(self, pwKeys):
        pwLen = len(self.password)
        keysLen = len(pwKeys)-1
        
        for i in range(pwLen):
            rand = random.randint(0, keysLen)
            self.password[i] = pwKeys[rand]
            
            print("DEBUG_JW: new pw key = ",pwKeys[rand])
            
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
    def __init__(self, pwLen, pwKeys):
        self.__password=[]
        self.__data = PasswordData(pwLen, pwKeys)

    def printWord(self):
        print("PW:\t", self.__data.password)
        
    def checkWholeWord(self, word):
        for i in range(0,len(self.__data.password)):
            if(self.__data.password[i]!=word[i]):
                return 0
        return 1
    
    def isCharInWord(self, char):
        for i in range(0,len(self.__data.password)):
            if(self.__data.password[i]== char):
                return True
        return False
    
    def isCharInWord_NEW(self, char, pos, wordDict):
        for i in range(0,len(self.__data.password)):
            if(self.__data.password[i]== char):
                return True
        return False

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
def destroy():
    print("Cleanup here...")
    
def guessPW(testPW, testWord):
    print("Guess:\t", testWord)
    result = testPW.getCompareResult(testWord)
    print("Result:\t", result)
    print("\n")


def PwTest():
    testPW = Password(TEST_PW_LEN, KEYS)
    testPW.printWord()
    print("\n")
    

    guessPW(testPW, ['0','0','0','0'])
    guessPW(testPW, ['1','1','1','1'])
    guessPW(testPW, ['2','2','2','2'])
    guessPW(testPW, ['1','2','3','4'])
    guessPW(testPW, ['A','#','B','C'])
    




if __name__ == '__main__':     # Program start from here
    try:
        PwTest()

    except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, cleanup.
        destroy()