from adafruit_circuitplayground import cp
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from random import randint
import usb_hid
import time

kbd = Keyboard(usb_hid.devices)

RED = (25, 0, 0)
GREEN = (0, 25, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

countdown = None
player_life = None
game_started = False
first_round = False

cp.pixels.brightness = 0.1

def press_key(key):
    if cp.switch:
        kbd.send(key)
        time.sleep(0.1)

def set_pixel_and_wait(color, duration):
    cp.pixels.fill(color)
    time.sleep(duration)
    cp.pixels.fill(BLACK)
    time.sleep(1)

def life_lost():
    global player_life
    print("Oh no!! The robot saw you and you lost a life :(")
    cp.play_tone(1200, 0.2)
    player_life -= 1
    set_pixel_and_wait(RED, 1)
    print("Only", player_life, "lives left!")

def start_game():
    global player_life, game_started
    cp.play_tone(1000, 0.2)
    press_key(Keycode.ZERO)
    press_key(Keycode.A)
    game_started = True
    player_life = 5

def reset_game():
    global countdown
    countdown = 3
    cp.pixels[0] = YELLOW
    wait = randint(2, 5)
    print("Waiting for",wait,"seconds")
    time.sleep(wait)

def end_game():
    global game_started
    press_key(Keycode.FIVE)
    cp.pixels.fill(RED)
    time.sleep(10)
    press_key(Keycode.ZERO)
    game_started = False

print("CP10: Main")

while True:
    if not game_started:
        cp.pixels[0] = RED
        if cp.button_a:
            start_game()
    else:
        reset_game()
        
        while countdown > 0:
            if countdown == 3:
                press_key(Keycode.TWO)
            else:
                cp.pixels[countdown] = BLACK
            for i in range(countdown):
                cp.pixels[i] = GREEN
            print(countdown)
            countdown -= 1
            cp.play_tone(500, 0.2)
            time.sleep(1)

        cp.pixels.fill(BLACK)
        timer_start = time.monotonic()

        print("The robot is looking, stay still!")
        cp.start_tone(100)

        while time.monotonic() - timer_start < 5:
            if not first_round:
                press_key(Keycode.THREE)
                first_round = True
            elif cp.shake(10):
                cp.stop_tone()
                life_lost()
                press_key(Keycode.FOUR)
                time.sleep(4)

        print("The robot is sleeping, hurry up!!!")
        cp.stop_tone()

        if player_life <= 0:
            end_game()
            break

    time.sleep(0.1)
