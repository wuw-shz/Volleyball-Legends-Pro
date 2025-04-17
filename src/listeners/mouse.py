import main
import win32gui
import concurrent.futures
from controller import MouseListener, Button

_executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)

def on_click(x: int, y: int, button: Button, pressed: bool):
    try:
        roblox_hwnd = win32gui.FindWindow(None, "Roblox")
        active_hwnd = win32gui.GetForegroundWindow()
        if roblox_hwnd != active_hwnd:
            return
         
        if main.shm.get(main.ShmVariable.isServing):
            if button == Button.left and pressed:
                if not main.shm.get(main.ShmVariable.isToss) and not main.shm.get(main.ShmVariable.isServe):
                    _executor.submit(main.toss)
        else:
            if button == Button.x1:
                main.isX1pressed = pressed
                _executor.submit(main.jump_set)
            elif button == Button.x2:
                main.isX2pressed = pressed
                _executor.submit(main.jump_spike)
            
    except AttributeError:
        pass

def start():
    listener = MouseListener(on_click=on_click)
    listener.daemon = True
    listener.start()
