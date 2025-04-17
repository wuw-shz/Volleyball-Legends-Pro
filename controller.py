import time
import ctypes
from pynput.keyboard import Key, KeyCode, Controller as KeyboardController, Listener as KeyboardListener
from pynput.mouse import Button, Controller as MouseController, Listener as MouseListener

class StaticDelegate(type):
    def __getattr__(cls, name):
        return getattr(cls._instance, name)

class mouse(metaclass=StaticDelegate):
    _instance = MouseController()
            
    @classmethod
    def position(cls):
        """The current position of the mouse pointer.

        This is the tuple ``(x, y)``, and setting it will move the pointer.
        """
        try:
            return cls._instance.position
        except Exception as e:
            print(f"Error getting mouse position: {e}")
            
    @classmethod
    def scroll(cls, dx: int, dy: int):
        """Sends scroll events.

        :param int dx: The horizontal scroll. The units of scrolling is
            undefined.

        :param int dy: The vertical scroll. The units of scrolling is
            undefined.

        :raises ValueError: if the values are invalid, for example out of
            bounds
        """
        try:
            cls._instance.scroll(dx, dy)
        except Exception as e:
            print(f"Error scrolling mouse: {e}")

            
    @classmethod
    def press(cls, button: Button):
        """Emits a button press event at the current position.

        :param Button button: The button to press.
        """
        try:
            cls._instance.press(button)
        except Exception as e:
            print(f"Error pressing mouse")
            
    @classmethod
    def release(cls, button: Button):
        """Emits a button release event at the current position.

        :param Button button: The button to release.
        """
        try:
            cls._instance.release(button)
        except Exception as e:
            print(f"Error releasing mouse")

    @classmethod
    def move(cls, dx: int, dy: int):
        """Moves the mouse pointer a number of pixels from its current
        position.

        :param int dx: The horizontal offset.

        :param int dy: The vertical offset.

        :raises ValueError: if the values are invalid, for example out of
            bounds
        """
        try:
            ctypes.windll.user32.mouse_event(0x0001, dx, dy, 0, 0)
        except Exception as e:
            print(f"Error moving mouse: {e}")

    @classmethod
    def click(cls, button: Button):
        """Emits a button click event at the current position.

        The default implementation sends a series of press and release events.

        :param Button button: The button to click.

        :param int count: The number of clicks to send.
        """
        try:
            cls._instance.click(button)
        except Exception as e:
            print(f"Error clicking mouse")

class keyboard(metaclass=StaticDelegate):
    _instance = KeyboardController()
            
    @classmethod
    def press(cls, key: Key):
        """Presses a key.

        A key may be either a string of length 1, one of the :class:`Key`
        members or a :class:`KeyCode`.

        Strings will be transformed to :class:`KeyCode` using
        :meth:`KeyCode.char`. Members of :class:`Key` will be translated to
        their :meth:`~Key.value`.

        :param key: The key to press.

        :raises InvalidKeyException: if the key is invalid

        :raises ValueError: if ``key`` is a string, but its length is not ``1``
        """
        try:
            cls._instance.press(key)
        except Exception as e:
            print(f"Error pressing key: {e}")
            
    @classmethod
    def release(cls, key: Key):
        """Releases a key.

        A key may be either a string of length 1, one of the :class:`Key`
        members or a :class:`KeyCode`.

        Strings will be transformed to :class:`KeyCode` using
        :meth:`KeyCode.char`. Members of :class:`Key` will be translated to
        their :meth:`~Key.value`.

        :param key: The key to release. If this is a string, it is passed to
            :meth:`touches` and the returned releases are used.

        :raises InvalidKeyException: if the key is invalid

        :raises ValueError: if ``key`` is a string, but its length is not ``1``
        """
        try:
            cls._instance.release(key)
        except Exception as e:
            print(f"Error releasing key: {e}")
    
    @classmethod
    def tap(cls, key: Key):
        """Presses and releases a key.

        This is equivalent to the following code::

            controller.press(key)
            controller.release(key)

        :param key: The key to press.

        :raises InvalidKeyException: if the key is invalid

        :raises ValueError: if ``key`` is a string, but its length is not ``1``
        """
        try:
            cls._instance.tap(key)
        except Exception as e:
            print(f"Error tapping key: {e}")
    
    @classmethod
    def touch(cls, key: Key):
        """Calls either :meth:`press` or :meth:`release` depending on the value
        of ``is_press``.

        :param key: The key to press or release.

        :param bool is_press: Whether to press the key.

        :raises InvalidKeyException: if the key is invalid
        """
        try:
            cls._instance.touch(key)
        except Exception as e:
            print(f"Error touching key: {e}")
    
    @classmethod
    def pressed(cls, *args):
        """Executes a block with some keys pressed.

        :param keys: The keys to keep pressed.
        """
        try:
            cls._instance.pressed(args)
        except Exception as e:
            print(f"Error pressed key: {e}")

    @classmethod
    def type(cls, text: str):
        """Types a string.

        This method will send all key presses and releases necessary to type
        all characters in the string.

        :param str string: The string to type.

        :raises InvalidCharacterException: if an untypable character is
            encountered
        """
        try:
            cls._instance.type(text)
        except Exception as e:
            print(f"Error typing text: {e}")

    @classmethod
    def hold(cls, key: Key, duration: float):
        try:
            cls._instance.press(key)
            time.sleep(duration)
            cls._instance.release(key)
        except Exception as e:
            print(f"Error holding key: {e}")

# def move_mouse(x, y):
#     try:
#         ctypes.windll.user32.mouse_event(0x0001, x, y, 0, 0)
#     except Exception as e:
#         print(f"Error moving mouse: {e}")