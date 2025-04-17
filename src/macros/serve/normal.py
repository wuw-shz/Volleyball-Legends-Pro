import main
import time
from controller import mouse, keyboard, Button, Key

def start():
    keyboard.tap('f')
    time.sleep(main.PING / 1000)
    time.sleep(0.2)
    keyboard.hold("s", 0.1)
    keyboard.hold("w", 0.2)
    keyboard.tap(Key.shift)
    time.sleep(0.05)
    keyboard.tap(Key.space)
    time.sleep(0.1)
    mouse.click(Button.left)
    keyboard.tap(Key.shift)

def toss():
    keyboard.tap('f')
    # keyboard.tap(Key.shift)
    # time.sleep(0.05)
    # for i in range(10):
    #     time.sleep(0.01)
    #     mouse.move(360, 0)
    # time.sleep(0.05)
    # keyboard.tap(Key.shift)