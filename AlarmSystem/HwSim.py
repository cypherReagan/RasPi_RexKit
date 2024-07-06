RASPI = True

if (RASPI):
    import LCD1602


#-------------------
# Keypad Simulation
#-------------------
SimKeys = []
if (not RASPI):
    # <Insert Desired Keypad Simulation Sequence Here>
    SimKeys = ['A']

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