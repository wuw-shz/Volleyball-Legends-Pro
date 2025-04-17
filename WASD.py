import ctypes
from pynput.keyboard import Controller as KeyboardController

keyboard = KeyboardController()

PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class HardwareInput(ctypes.Structure):
    _fields_ = [
        ("uMsg", ctypes.c_ulong),
        ("wParamL", ctypes.c_short),
        ("wParamH", ctypes.c_ushort)
    ]

class MouseInput(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]

class Input_I(ctypes.Union):
    _fields_ = [
        ("ki", KeyBdInput),
        ("mi", MouseInput),
        ("hi", HardwareInput)
    ]

class Input(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("ii", Input_I)
    ]

def send_key(scancode, flags):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, scancode, flags, 0, ctypes.pointer(extra))
    x = Input(1, ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def press_key(scancode):
    send_key(scancode, 0x0008)

def release_key(scancode):
    send_key(scancode, 0x0008 | 0x0002)

SCANCODES = {
    'w': 0x11,
    'a': 0x1E,
    's': 0x1F,
    'd': 0x20
}

GROUPS = {
    'w': 'WS',
    's': 'WS',
    'a': 'AD',
    'd': 'AD'
}

held_keys = {
    'WS': [],
    'AD': []
}
active_key = {
    'WS': None,
    'AD': None
}

def on_press(key):
    try:
        k = key.char.lower()
    except AttributeError:
        return

    if k not in SCANCODES:
        return

    group = GROUPS[k]
    if k not in held_keys[group]:
        held_keys[group].append(k)
        if active_key[group] is not None:
            if active_key[group] != k:
                keyboard.release(active_key[group])
                keyboard.press(k)
                # release_key(SCANCODES[active_key[group]])
                # press_key(SCANCODES[k])
                active_key[group] = k
        else:
            active_key[group] = k

def on_release(key):
    try:
        k = key.char.lower()
    except AttributeError:
        return

    if k not in SCANCODES:
        return

    group = GROUPS[k]
    if k in held_keys[group]:
        held_keys[group].remove(k)
        if active_key[group] == k:
            # release_key(SCANCODES[k])
            keyboard.release(k)
            if held_keys[group]:
                new_active = held_keys[group][-1]
                # release_key(SCANCODES[new_active])
                # press_key(SCANCODES[new_active])
                keyboard.press(new_active)
                keyboard.release(k)
                active_key[group] = new_active
            else:
                active_key[group] = None