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
    global countdown, three_key_pressed
    countdown = 3
    cp.pixels.fill(black)
    wait = random.randint(2, 5)
    time.sleep(wait)
    three_key_pressed = False


def send_message(char, msg):
    global delimiter
    data = char + delimiter + msg
    uart.write(data.encode("utf-8"))
    print("Sending:", data)
    time.sleep(0.1)


def press_key(key):
    if cp.switch:
        kbd.send(key)
        time.sleep(0.1)


def light_up_pixels(color, duration):
    cp.pixels.fill(color)
    time.sleep(duration)
    cp.pixels.fill(black)
    time.sleep(1)


def get_parts():
    received_data = uart.readline()
    if received_data:
        decoded_data = received_data.decode("utf-8").strip()
        return decoded_data.split(",")
    return []


def start_countdown():
    global countdown
    while countdown >= 0:
        if countdown == 3:
            press_key(Keycode.TWO)
            # Sending info
            send_message("C", str(randint(0, 9)))
        else:
            cp.pixels[countdown] = black
        for i in range(countdown - 1):
            cp.pixels[i] = green
        print(countdown)
        countdown -= 1
        time.sleep(1)
    cp.pixels.fill(black)


def game_over():
    press_key(Keycode.FIVE)
    cp.pixels.fill(red)
    time.sleep(10)
    press_key(Keycode.ZERO)


def shake():
    global LifeCounter
    # Sending info
    send_message("P", str(randint(0, 9)))
    # Light Up Pixels
    light_up_pixels(red, 1)
    # time.sleep(4)
    LifeCounter -= 1


# Flag to track whether the game is active
game_active = False
shaken = False

while True:

    if cp.button_a and not game_active:
        press_key(Keycode.ZERO)
        game_active = True
        print("Game Start!")
        press_key(Keycode.A)  # Press the "A" key at the start of the game
        # time.sleep(18)
        countdown = 3
        LifeCounter = 5

    if game_active:

        press_key(Keycode.ONE)

        reset()  # Call the reset function at the start of each loop iteration

        start_countdown()
        timer_start = time.monotonic()
        print("START TIMER")

        while time.monotonic() - timer_start < 5:
            print("READY TO SHAKE")

            if three_key_pressed is False:  # Check if "3" key hasn't been pressed
                press_key(Keycode.THREE)
                three_key_pressed = True  # Set the flag to indicate it has been pressed
                send_message("S", str(randint(0, 9)))

            if cp.shake(10):
                shake()
                press_key(Keycode.FOUR)  # Video
                time.sleep(4)

        if uart.in_waiting:
            parts = get_parts()

            for part in parts:
                print("Received:", part)
                if part == "W":
                    cp.pixels.fill(green)
                    time.sleep(10)
                    break
                if part == "P":
                    cp.pixels.fill(red)
                    time.sleep(1)

        # print("Lives left:", LifeCounter)

        if LifeCounter <= 0:
            game_over()
            break

    time.sleep(0.1)# Write your code here :-)
