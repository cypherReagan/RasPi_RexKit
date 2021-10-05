#!/usr/bin/env python3
import RPi.GPIO as GPIO
from time import time

#IrPin  = 11
IrPin  = 11 # GPPIO 17
count = 0

def setup():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    #GPIO.setup(IrPin, GPIO.IN, pull_up_down=GPIO.PUD_UP) # orig code
    GPIO.setup(IrPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def irEventHandler(ev=None):
    global count
    count += 1
    #print ('Received infrared. count = ', count)
    
    code = irReceive(IrPin, GPIO.FALLING)
    if (code):
        print(str(hex(code)))
        print(str(bin(code)))
    else:
        print("Invalid code")

def loop():
    
    try:
        GPIO.add_event_detect(IrPin, GPIO.FALLING, callback=irEventHandler) # wait for falling
        print("Starting IR Listener...")
        while True:
            pass   # Don't do anything
            #print("Waiting for signal...")
    except KeyboardInterrupt:
        # User pressed CTRL-C
        # Reset GPIO settings
        print("Ctrl-C pressed!")
    except RuntimeError:
        # this gets thrown when control C gets pressed
        # because wait_for_edge doesn't properly pass this on
        pass
    print("Quitting")
    destroy()

def binaryAquire(pin, duration):
    # aquires data as quickly as possible
    time0 = time()
    results = []
    while ((time() - time0) < duration):
        results.append(GPIO.input(pin))
    return results

def irReceive(pinNum, bounceTime=150):
    # when edge detect is called (which requires less CPU than constant
    # data acquisition), we acquire data as quickly as possible
    data = binaryAquire(pinNum, bounceTime/1000.0)
    oldVal = 1
    lastIndex = 0
    index = 0
    
    print('len data, data: ', len(data), data)
    #print('len gaps,gaps',len(gaps),gaps)
    if (len(data) < bounceTime):
        return
    
    rate = len(data) / (bounceTime / 1000.0)
    pulses = []
    iBreak = 0
    
    # detect run lengths using the acquisition rate to convert the times into microseconds
    for i in range(1, len(data)):
        if (data[i] != data[i-1]) or (i == len(data)-1):
            pulses.append((data[i-1], int((i-iBreak)/rate*1e6)))
            iBreak = i
         
    outBin = ""
    for val, uSec in pulses:
        if (val != 1):
            continue
        if (outBin and uSec > 2000):
            break
        elif (uSec < 1000):
            outBin += "0"
        elif (1000 < uSec < 2000):
            outBin += "1"
        else:
            print("DEBUG_JW: irReceive() - outBin not handled! val = {val}")

        try:
            return int(outBin, 2)
        except ValueError:
            # probably an empty code
            print("DEBUG_JW: irReceive() - ValueError")
            return None
    

def destroy():
    GPIO.cleanup()                     # Release resource

if __name__ == '__main__':     # Program start from here
    setup()
    loop()