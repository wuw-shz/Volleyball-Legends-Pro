import main
import time
import threading
from controller import mouse, keyboard, Button, Key

def left_click():
   mouse.click(Button.left)

def start():
   if main.isX2pressed:
      if main.isX1pressed:
         main.jumpspikeMode = True
      else:
         keyboard.tap(Key.shift)
         time.sleep(0.05)
         # keyboard.tap(Key.ctrl)
         # time.sleep(0.05)
         keyboard.tap(Key.space)
         # time.sleep(0.05)
         # keyboard.press('s')
   else:
      if main.jumpsetMode:
         keyboard.release("e")
      else:
         if not main.isX1pressed:
            keyboard.tap(Key.shift)
         threading.Thread(target=left_click, daemon=True).start()
         # time.sleep(0.05)
         # keyboard.release("s")
         main.jumpspikeMode = False