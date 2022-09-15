import random


keys =     ['1','2','3','A',
            '4','5','6','B',
            '7','8','9','C',
            '*','0','#','D']

#testWord=['0','0','0','0']
TEST_PW_LEN = 4

class Password(object):
    
    INCORRECT_CHAR = 'X'
    CORRECT_CHAR = 'C'
    
    #constructor
    def __init__(self, pwLen, pwKeys):
        self.__password=[]
        
        if (pwLen <= 0):
            print("ERROR: invalid PW len ",pwLen)
        else:
            count = 0
            while (count < pwLen):
                count += 1
                self.__password.append('0')
                
            self.generateWord(pwKeys)

    def printChars(self):
        print("PW:\t", self.__password)
        
    def generateWord(self, pwKeys):
        pwLen = len(self.__password)
        keysLen = len(pwKeys)-1
        
        for i in range(pwLen):
            rand = random.randint(0, keysLen)
            self.__password[i] = pwKeys[rand]
        
    def checkWholeWord(self, word):
        for i in range(0,len(self.__password)):
            if(self.__password[i]!=word[i]):
                return 0
        return 1

    def getGuessResult(self, word):
        result = []
        
        pwLen = len(self.__password)
        
        for i in range(0, pwLen):
            if (self.__password[i] == word[i]):
                result.append(self.CORRECT_CHAR)
            else:
                result.append(self.INCORRECT_CHAR)
        
        return result

def destroy():
    print("Cleanup here...")
    
def guessPW(testPW, testWord):
    print("Guess:\t", testWord)
    result = testPW.getGuessResult(testWord)
    print("Result:\t", result)
    print("\n")


def PwTest():
    testPW = Password(TEST_PW_LEN, keys)
    testPW.printChars()
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