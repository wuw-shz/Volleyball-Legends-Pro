import main
import time
from controller import mouse, keyboard, Key

def start():
   keyboard.tap(Key.esc)
   time.sleep(0.05)
   keyboard.tap("r")
   keyboard.tap("r")
   keyboard.tap(Key.enter)