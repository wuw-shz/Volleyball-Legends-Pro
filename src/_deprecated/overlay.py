import main
import ctypes
import win32gui
import win32con
import tkinter as tk
from src.sharedMemory.SharedMemory import shm, ShmVariable

OVERLAY_WIDTH = 800
OVERLAY_HEIGHT = 600
OVERLAY_OFFSET_X = 100
OVERLAY_OFFSET_Y = 100
OVERLAY_BG_COLOR = "white"
OVERLAY_TITLE = "Overlay"

def start():
   overlay_ui_loop()

def overlay_ui_loop():
   root = tk.Tk()
   root.overrideredirect(True)
   root.wm_attributes("-topmost", True)
   root.wm_attributes("-transparentcolor", OVERLAY_BG_COLOR)
   root.geometry(f"{OVERLAY_WIDTH}x{OVERLAY_HEIGHT}+{OVERLAY_OFFSET_X}+{OVERLAY_OFFSET_Y}")
   root.title(OVERLAY_TITLE)
   canvas = tk.Canvas(root, width=OVERLAY_WIDTH, height=OVERLAY_HEIGHT,
                     bg=OVERLAY_BG_COLOR, highlightthickness=0)
   canvas.pack(fill="both", expand=True)

   line_id = canvas.create_line(OVERLAY_WIDTH // 2, 0, OVERLAY_WIDTH // 2, OVERLAY_HEIGHT,
                                 fill="red", width=1)
   serve_text_id = canvas.create_text(OVERLAY_WIDTH - 5, 5, text="", font=("Arial", 30),
                                       anchor="ne")

   root.update_idletasks()
   hwnd = ctypes.windll.user32.FindWindowW(None, OVERLAY_TITLE)
   if hwnd:
      make_click_through(hwnd)
   else:
      print("Could not find overlay window handle.")

   update_overlay(root, canvas, line_id, serve_text_id)
   root.mainloop()

def make_click_through(hwnd: int):
   try:
      styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
      new_styles = styles | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
      win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_styles)
   except Exception as e:
      print(f"Error setting click-through for window: {e}")

def get_serve_mode_text():
   if main.serveMode == 1:
      return "Normal"
   elif main.serveMode == 2:
      return "Advanced"
   else:
      return "Skill"

def update_overlay(root: tk.Tk, canvas: tk.Canvas, line_id: int, serve_text_id: int):
   roblox_hwnd = win32gui.FindWindow(None, "Roblox")
   if roblox_hwnd:
      try:
         x, y, x2, y2 = win32gui.GetWindowRect(roblox_hwnd)
         width, height = x2 - x, y2 - y

         root.geometry(f"{width}x{height}+{x}+{y}")
         canvas.config(width=width, height=height)

         canvas.coords(line_id, width // 2, 0, width // 2, height // 2)
         canvas.coords(serve_text_id, width - 10, height // 2)
         serve_text = get_serve_mode_text()
         text_color = "green" if shm.get(ShmVariable.isServing) else "red"
         canvas.itemconfigure(serve_text_id, text=serve_text, fill=text_color)

         active_hwnd = win32gui.GetForegroundWindow()
         if active_hwnd == roblox_hwnd:
               canvas.itemconfigure(line_id, state="normal")
               canvas.itemconfigure(serve_text_id, state="normal")
         else:
               canvas.itemconfigure(line_id, state="hidden")
               canvas.itemconfigure(serve_text_id, state="hidden")
      except Exception as e:
         print(f"Error updating overlay: {e}")
   else:
      canvas.itemconfigure(line_id, state="hidden")
      canvas.itemconfigure(serve_text_id, state="hidden")
   
   root.after(100, update_overlay, root, canvas, line_id, serve_text_id)