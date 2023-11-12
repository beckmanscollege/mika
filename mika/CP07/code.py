from adafruit_circuitplayground import cp
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_motor import servo
from digitalio import DigitalInOut, Direction, Pull

import usb_hid
import time
import board
import pwmio
import busio

pwm = pwmio.PWMOut(board.A2, duty_cycle=2 ** 15, frequency=50)

my_servo = servo.Servo(pwm)

kbd = Keyboard(usb_hid.devices)
uart = busio.UART(board.TX, board.RX, baudrate=115200)

angle = 0

btnA_pressed = False

btn1 = DigitalInOut(board.A4)
btn1.direction = Direction.INPUT
btn1.pull = Pull.UP
btn1_pressed = False

btn2 = DigitalInOut(board.A5)
btn2.direction = Direction.INPUT
btn2.pull = Pull.UP
btn2_pressed = False

def clear_uart_buffer():
    while uart.in_waiting > 0:
        uart.read(1)

def send_message(data):
    uart.write(data.encode("utf-8"))
    print("Sending:", data)
    time.sleep(0.2)

print("CP07: Win mechanism")

def clamp(n, minn, maxn):
    if n < minn:
        return minn
    elif n > maxn:
        return maxn
    else:
        return n


while True:

    if cp.button_a and not btnA_pressed:
        clear_uart_buffer() 
        send_message("W")
        btnA_pressed = True
    else:
        btnA_pressed = False

    if not btn1.value and not btn1_pressed:
            kbd.send(Keycode.RIGHT_ARROW)
            btn1_pressed = True
            my_servo.angle = 90
    else:
        btn1_pressed = False

    if not btn2.value and not btn2.pressed:
            btn2_pressed = True
            my_servo.angle = 0
    else:
        btn2_pressed = False

    angle = clamp(angle, 0, 180)
    my_servo.angle = angle
    time.sleep(0.1)