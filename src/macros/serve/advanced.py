import main
import time
import numpy as np
from controller import mouse, keyboard, Button, Key

# def start():
#     keyboard.tap('f')
#     keyboard.tap(Key.shift)
#     keyboard.release('w')
#     time.sleep(main.PING / 1000)
#     keys = ['a', 'w', 'd', 's', 's'] if np.random.randint(0, 2) == 0 else ['d', 'w', 'a', 's', 's']
#     for key in keys:
#         keyboard.hold(key, 0.08)
#     keyboard.press('w')
#     keyboard.tap(Key.shift)
#     time.sleep(0.1)
#     keyboard.tap(Key.space)
#     time.sleep(0.5)
#     mouse.click(Button.left)
#     time.sleep(0.05)
#     keyboard.release('w')
#     time.sleep(0.05)
#     keyboard.tap(Key.shift)

def start():
    keyboard.tap('f')
    keyboard.release('w')
    time.sleep(main.PING / 1000)
    time.sleep(0.05)
    mouse.move(-200, 0)
    keyboard.tap(Key.shift)
    keyboard.hold('d', 0.3)
    keyboard.tap(Key.shift)
    time.sleep(0.05)
    keyboard.press('w')
    keyboard.press('a')
    mouse.move(-210, 0)
    time.sleep(0.05)
    keyboard.tap(Key.space)
    time.sleep(0.05)
    keyboard.release('a')
    time.sleep(0.3)
    mouse.click(Button.left)
    time.sleep(0.05)
    keyboard.release('w')
    time.sleep(0.05)
    keyboard.tap(Key.shift)

def toss():
    keyboard.tap(Key.shift)
    time.sleep(0.05)
    mouse.move(400, 0)
    time.sleep(0.05)
    keyboard.tap('f')
    keyboard.press('w')