import main
import win32gui
import WASD as wasd
from concurrent.futures import ThreadPoolExecutor
from controller import KeyboardListener, Key, KeyCode, keyboard

_executor = ThreadPoolExecutor(max_workers=5)
last_r_press_time = 0

def on_press(key: Key | KeyCode):
    global last_r_press_time
    try:
        roblox_hwnd = win32gui.FindWindow(None, "Roblox")
        active_hwnd = win32gui.GetForegroundWindow()
        if roblox_hwnd != active_hwnd:
            return
        if key == Key.f1:
            main.shm.set(main.ShmVariable.isToss, False)
            main.shm.set(main.ShmVariable.isServe, False)
            main.shm.set(main.ShmVariable.isServing, False)
            main.shm.set(main.ShmVariable.isInServeLoop, False)
        elif key == Key.f4:
            _executor.submit(main.reset)
        elif hasattr(key, 'char') and key.char and key.char.lower() == 'z':
            serveMode = main.shm.get(main.ShmVariable.serveMode)
            # shm.set(ShmVariable.serveMode, 1 if (serveMode == 3) else (serveMode + 1))
            main.shm.set(main.ShmVariable.serveMode, 1 if (serveMode == 3) else (serveMode + 1))


        # wasd.on_press(key)
    except AttributeError:
        pass

def on_release(key: Key | KeyCode):
    try:
        roblox_hwnd = win32gui.FindWindow(None, "Roblox")
        active_hwnd = win32gui.GetForegroundWindow()
        if roblox_hwnd == active_hwnd:
            wasd.on_release(key)
    except AttributeError:
        pass

def start() -> None:
    listener = KeyboardListener(
        on_press=on_press,
        # on_release=on_release
    )
    listener.daemon = True
    listener.start()
