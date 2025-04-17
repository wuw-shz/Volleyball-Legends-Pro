import cv2
import main
import time
import win32gui
import pyautogui
import numpy as np
import pygetwindow as gw
import threading

def start():
    toss_loop()

tossImg = cv2.imread("assets/1920x1080/normal/toss.png", cv2.IMREAD_COLOR)
serveImg = cv2.imread("assets/1920x1080/normal/serve.png", cv2.IMREAD_COLOR)

if tossImg is None or serveImg is None:
    print("One or both template images not found!")
    exit()

threshold = 0.9

def get_roblox_window():
    roblox_hwnd = win32gui.FindWindow(None, "Roblox")
    active_hwnd = win32gui.GetForegroundWindow()
    if active_hwnd == roblox_hwnd:
        try:
            win = gw.getWindowsWithTitle("Roblox")[0]
            return win.left, win.top, win.width, win.height
        except Exception as e:
            print(f"Error getting window: {e}")
    return None

def toss_loop():
    while True:
        window_coords = get_roblox_window()
        if window_coords:
            left, top, width, height = window_coords
            region1 = (left, top, width, height)
            # region1 = (left + (width // 2) - 32, top + height - 24, 55, 13) # 1604x720
            # region1 = (674, 608, 50, 13) # 1404x630 
            # region1 = (677, 611, 44, 10) # 1404x630 new
            # region1 = (642, 744, 72, 10)  # 1366x768
            # region1 = (915, 1048, 81, 14) # 1920x1080
            region1 = (918, 1050, 74, 11) # 1920x1080 normal
            try:
                screenshot1 = pyautogui.screenshot(region=region1)
                screenshot_cv1 = cv2.cvtColor(np.array(screenshot1), cv2.COLOR_RGB2BGR)
                result1 = cv2.matchTemplate(screenshot_cv1, tossImg, cv2.TM_CCOEFF_NORMED)
                _, max_val1, _, max_loc = cv2.minMaxLoc(result1)
                if max_val1 >= threshold:
                    # print((max_loc[0], max_loc[1], tossImg.shape[1], tossImg.shape[0]), max_val1)
                    main.isServing = True
                    if not main.isInServeLoop:
                        threading.Thread(target=serve_loop, daemon=True).start()
                else:
                    main.isServing = False
                    main.isServe = False
                    main.isToss = False
            except Exception as e:
                print(f"Error in toss detection: {e}")
        time.sleep(0.2)

def serve_loop():
    while True:
        main.isInServeLoop = True
        window_coords = get_roblox_window()
        if not main.isServing:
            main.isInServeLoop = False
            break
        if window_coords and main.isServing and not main.isServe:
            left, top, width, height = window_coords
            region2 = (left, top, width, height)
            # region2 = (left + (width // 2) - 95, top + height - 156, 125, 55) # 1604x720
            # region2 = (615, 493, 18, 8) # 1404x630
            # region2 = (595, 602, 29, 11) # 1366x768
            # region2 = (853, 849, 27, 13) # 1920x1080
            region2 = (855, 850, 34, 12) # 1920x1080 normal
            try:
                screenshot2 = pyautogui.screenshot(region=region2)
                screenshot_cv2 = cv2.cvtColor(np.array(screenshot2), cv2.COLOR_RGB2BGR)
                result2 = cv2.matchTemplate(screenshot_cv2, serveImg, cv2.TM_CCOEFF_NORMED)
                _, max_val2, _, max_loc = cv2.minMaxLoc(result2)
                if max_val2 >= threshold:
                    # print((max_loc[0], max_loc[1], serveImg.shape[1], serveImg.shape[0]), max_val2)
                    time.sleep(0.48)
                    main.serve()
                    main.isInServeLoop = False
                    break
            except Exception as e:
                print(f"Error in serve detection: {e}")
        time.sleep(0.05)