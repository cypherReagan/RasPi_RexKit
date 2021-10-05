#!/usr/bin/env python3

import time
import smbus

BUS = smbus.SMBus(1)
I2C_PERIPHERAL_ADDR = 0x27


def write_word(addr, data):
    print("DEBUG_JW: LCD1602->write_word()")
    global BLEN
    temp = data
    if BLEN == 1:
        temp |= 0x08
    else:
        temp &= 0xF7
    BUS.write_byte(addr ,temp)

def send_command(comm):
    print("DEBUG_JW: LCD1602->send_command()")
    # Send bit7-4 firstly
    buf = comm & 0xF0
    buf |= 0x04               # RS = 0, RW = 0, EN = 1
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               # Make EN = 0
    write_word(LCD_ADDR ,buf)

    # Send bit3-0 secondly
    buf = (comm & 0x0F) << 4
    buf |= 0x04               # RS = 0, RW = 0, EN = 1
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               # Make EN = 0
    write_word(LCD_ADDR ,buf)

def send_data(data):
    print("DEBUG_JW: LCD1602->send_data()")
    # Send bit7-4 firstly
    buf = data & 0xF0
    buf |= 0x05               # RS = 1, RW = 0, EN = 1
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               # Make EN = 0
    write_word(LCD_ADDR ,buf)

    # Send bit3-0 secondly
    buf = (data & 0x0F) << 4
    buf |= 0x05               # RS = 1, RW = 0, EN = 1
    write_word(LCD_ADDR ,buf)
    time.sleep(0.002)
    buf &= 0xFB               # Make EN = 0
    write_word(LCD_ADDR ,buf)

def init(addr, bl):
    #global BUS
    #BUS = smbus.SMBus(1)
    print("DEBUG_JW: LCD1602->init()")
    global LCD_ADDR
    global BLEN
    LCD_ADDR = addr
    BLEN = bl
    try:
        send_command(0x33) # Must initialize to 8-line mode at first
        time.sleep(0.005)
        send_command(0x32) # Then initialize to 4-line mode
        time.sleep(0.005)
        send_command(0x28) # 2 Lines & 5*7 dots
        time.sleep(0.005)
        send_command(0x0C) # Enable display without cursor
        time.sleep(0.005)
        send_command(0x01) # Clear Screen
        BUS.write_byte(LCD_ADDR, 0x08)
    except:
        print("DEBUG_JW: LCD1602->init() - exception occurred!")
        return False
    else:
        return True

def clear():
    print("DEBUG_JW: LCD1602->clear()")
    send_command(0x01) # Clear Screen

def openlight():  # Enable the backlight
    print("DEBUG_JW: LCD1602->openlight()")
    BUS.write_byte(I2C_PERIPHERAL_ADDR,0x08)
    #BUS.close()

def write(x, y, str):
    print("DEBUG_JW: LCD1602->write()")
    if x < 0:
        x = 0
    if x > 15:
        x = 15
    if y <0:
        y = 0
    if y > 1:
        y = 1

    # Move cursor
    addr = 0x80 + 0x40 * y + x
    send_command(addr)

    for chr in str:
        send_data(ord(chr))

if __name__ == '__main__':
    print("DEBUG_JW: LCD1602->main() - start!")
    init(0x27, 1)
    
    openlight()
    write(4, 0, 'Hello')
    write(7, 1, 'REXQUALIS!')
    
