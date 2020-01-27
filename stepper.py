#!/usr/bin/env python3
import sys, tty, termios, time, pigpio
pi = pigpio.pi()
if pi.connected:
    print("Connected to pigpio daemon!\n")
    print("""
         f to set Frequency
         p to set Dutycycle percentage
         w to increment Frequency
         s to decrement Frequency
         a to decrement Dutycycle
         d to increment Dutycycle
         r to toggle motor direction
         spacebar to pause/unpause motor
         numbers 1 2 4 6 8 0 to multiply w/s/a/d increments by 1 2 4 6 8 or 10
         x to exit
        """)

# Variables
global pw
global hz
global oldhz
global dirpin
global mult
global paused
pw = 50
hz = 0
oldhz = 0
dirpin = 0
mult = 1
paused = 0

# Definitions
def set():
    global pw
    global hz
    global dirpin
    if pw > 100:
        pw = 100
    if pw < 0:
        pw = 0
    if hz < 0:
        hz = 0
    print(hz, "hz", pw, "%", "Direction:", dirpin)
    pi.hardware_PWM(18, hz, pw*10000)

def pause():
    global hz
    global oldhz
    global paused
    if(paused == 0):
        oldhz = hz
        hz = 0
        set()
    if(paused == 1):
        hz = oldhz
        set()
    paused ^= 1

# The getch method can determine which key has been pressed
# by the user on the keyboard by accessing the system files
# It will then return the pressed key as a variable
def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

# Main loop
try:
    while True:
        # Keyboard character retrieval method is called and saved into variable
        char = getch()
        # f to directly set freq
        if(char == "f"):
            hz = input("Frequency?: ")
            hz = int(hz)
            set()
        # p to directly set PWM duty cycle
        if(char == "p"):
            pw = input("Dutycycle%?: ")
            pw = int(pw)
            set()
        if(char == "m"):
            mult = input("Multiplier?: ")
            mult = int(mult)
            print("Multiplier set to", mult)
        # w to increment freq
        if(char == "w"):
            hz += 1*mult
            set()
        # s to decrement freq
        if(char == "s"):
            hz -= 1*mult
            set()
        # a to decrement dutycycle
        if(char == "a"):
            pw -= 1*mult
            set()
        # d to increment dutycycle
        if(char == "d"):
            pw += 1*mult
            set()
        # r to toggle GPIO 17 for motor driver direction pin
        if(char == "r"):
            dirpin ^= 1
            pi.write(17,dirpin)
            print("Direction set to", dirpin)
        # spacebar to pause/unpause motor
        if(char == " "):
            pause()
            print(hz, "hz", pw, "%", "Direction:", dirpin)
        # mults
        if(char == "1"):
            mult = 1
            print("Multiplier set to", mult)
        if(char == "2"):
            mult = 2
            print("Multiplier set to", mult)
        if(char == "4"):
            mult = 4
            print("Multiplier set to", mult)
        if(char == "6"):
            mult = 6
            print("Multiplier set to", mult)
        if(char == "8"):
            mult = 8
            print("Multiplier set to", mult)
        if(char == "0"):
            mult = 10
            print("Multiplier set to", mult)
        # x to exit
        if(char == "x"):
            break
except KeyboardInterrupt:
    print ("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
finally:
    pi.hardware_PWM(18, 0, 500000)
    pi.stop()
