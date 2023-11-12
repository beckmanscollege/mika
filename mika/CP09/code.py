from adafruit_circuitplayground import cp
from random import randint
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

import usb_hid
import board
import busio
import time
import random

# KBD
kbd = Keyboard(usb_hid.devices)

# Colours
red = (25, 0, 0)
green = (0, 25, 0)
black = (0, 0, 0)

# Counters
countdown = 3
LifeCounter = 5

# Variables
WakingUp = False
RedLight_On = False

# Track whether key has been pressed
one_key_pressed = False
three_key_pressed = False

uart = busio.UART(board.TX, board.RX, baudrate=115200)
delimiter = ","

# THIS IS CODE FOR CP10, MAIN UNIT
print("CP10")

def reset():
    print("reset")
    global countdown
    countdown = 3
    cp.pixels.fill(black)
    wait = random.randint(10, 15)
    time.sleep(wait)
    three_key_pressed = False

# Function to play the BLANK video
def press_zero_key():
    kbd.press(Keycode.ZERO)
    kbd.release_all()

# Function to play the IDLE video
def press_one_key():
    kbd.press(Keycode.ONE)
    kbd.release_all()

# Function to play the WAKEUP video
def press_two_key():
    kbd.press(Keycode.TWO)
    kbd.release_all()

# Function to play the AWAKE video
def press_three_key():
    kbd.press(Keycode.THREE)
    kbd.release_all()

# Function to play the ATTACK video
def press_four_key():
    kbd.press(Keycode.FOUR)
    kbd.release_all()

# Function to play the DEATH video
def press_five_key():
    kbd.press(Keycode.FIVE)
    kbd.release_all()

# Function to play the WIN video
def press_six_key():
    kbd.press(Keycode.SIX)
    kbd.release_all()

# Function to play the ALIVE video
def press_A_key():
    kbd.press(Keycode.A)
    kbd.release(Keycode.A)

# Flag to track whether the game is active
game_active = False

while True:

    if cp.button_a and not game_active:
        press_zero_key
        game_active = True
        print("Game Start!")

        # Press the "A" key at the start of the game
        press_A_key()

        # Sleep for 5 seconds
        time.sleep(18)

        countdown = 3
        LifeCounter = 5

    if game_active:

        # Press the "1" key at the start of each loop iteration
        press_one_key()

        reset()  # Call the reset function at the start of each loop iteration

        while countdown >= 0:
            if countdown == 3:
                press_two_key()
                # Sending info
                random_number = randint(0, 9)
                data = "C" + delimiter + str(random_number)
                print("Sending:", data)
                uart.write(data.encode("utf-8"))
            else:
                cp.pixels[countdown] = black
            for i in range(countdown - 1):
                cp.pixels[i] = green
            print(countdown)
            countdown -= 1
            time.sleep(1)

        cp.pixels.fill(black)
        timer_start = time.monotonic()
        print("timer_start")

        while time.monotonic() - timer_start < 5:
            print("ready to shake")
            if three_key_pressed is False:  # Check if "3" key hasn't been pressed
                press_three_key()
                three_key_pressed = True  # Set the flag to indicate it has been pressed
                # Sending info
                random_number = randint(0, 9)
                data = "S" + delimiter + str(random_number)
                print("Sending:", data)
                uart.write(data.encode("utf-8"))

            if cp.shake(10):
                cp.play_tone(666,1)
                # RedLight ON
                RedLight_On = True
                # Video
                press_four_key()
                # Sending info
                random_number = randint(0, 9)
                data = "P" + delimiter + str(random_number)
                print("Sending:", data)
                uart.write(data.encode("utf-8"))
                # Light Up Pixels
                cp.pixels.fill(red)
                time.sleep(1)
                cp.pixels.fill(black)
                time.sleep(4)
                # LifeCounter
                LifeCounter -= 1
            else:
                RedLight_On = False
                # RECEIVE CODE


        # TRANSMIT CODE
        # if cp.button_a and not button_a_pressed:
        #    button_a_pressed = True
        #    random_number = randint(0, 9)
        #    data = "P" + delimiter + str(random_number)
        #    print("Sending:", data)
        #    uart.write(data.encode("utf-8"))
        # else:
        #    button_a_pressed = False

        print("Lives left:", LifeCounter)

        if LifeCounter <= 0:
            press_five_key()
            cp.pixels.fill(red)
            time.sleep(10)
            press_zero_key

            break

    time.sleep(0.1)
