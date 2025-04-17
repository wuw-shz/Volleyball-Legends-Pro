import main
import time
import threading
from controller import mouse, keyboard, Button, Key

def left_click():
   mouse.click(Button.left)

def start():
   if main.isX1pressed:
      if main.isX2pressed:
         keyboard.press("e")
         main.jumpsetMode = True
      else:
         keyboard.tap(Key.shift)
         time.sleep(0.05)
         keyboard.tap(Key.space)
         time.sleep(0.05)
         keyboard.press("e")
   else:
      if main.jumpspikeMode:
         threading.Thread(target=left_click, daemon=True).start()
      else:
         if not main.isX2pressed:
            keyboard.tap(Key.shift)
         keyboard.release("e")
         # keyboard.tap('e')
         main.jumpsetMode = False