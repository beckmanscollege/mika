import usb_hid

from adafruit_circuitplayground import cp
from random import randint
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

import board
import busio

kbd = Keyboard(usb_hid.devices)

is_touched = False

uart = busio.UART(board.TX, board.RX, baudrate=115200)
delimiter = ","

# THIS CODE IS FOR CP07, THE WIN MECHANISM
print("CP07")

while True:
    if uart.in_waiting:
        received_data = uart.readline()
        decoded_data = received_data.decode("utf-8").strip()
        parts = decoded_data.split(",")

    if cp.touch_A1:
        kbd.send(Keycode.SIX)
        random_number = randint(0, 9)
        data = "W" + delimiter + str(random_number)
        print("Sending:", data)
        uart.write(data.encode("utf-8"))
    else:
        kbd.release(Keycode.SIX)
