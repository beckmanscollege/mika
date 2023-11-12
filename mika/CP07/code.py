import usb_hid
from adafruit_circuitplayground import cp
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
import board
import busio
import time

kbd = Keyboard(usb_hid.devices)
uart = busio.UART(board.TX, board.RX, baudrate=115200)
delimiter = ","

def send_message(char, msg=None):
    global delimiter
    msg = str(msg) if msg is not None else ""
    data = f"{char}{delimiter}{msg}"
    uart.write(data.encode("utf-8"))
    print("Sending:", data)
    time.sleep(0.2)

print("CP07: Win mechanism")

btn_pressed = False

while True:
    if cp.button_a and not btn_pressed:
        send_message("W")
        btn_pressed = True
    else:
        btn_pressed = False
