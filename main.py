import os
import time
import threading
import subprocess
import atexit
from src.ui import terminal
from src.listeners import mouse, keyboard
from src.macros.serve import normal, advanced, skill
from src.macros import serves, jumpset, jumpspike, resets
from src.sharedMemory.SharedMemory import  shm, ShmVariable

PING = 50
jumpsetMode = False
jumpspikeMode = False
isX1pressed = False
isX2pressed = False

processes: list[subprocess.Popen] = []

def toss():
    try:
        serves.toss()
    except Exception as e:
        print(f"Error in toss: {e}")

def serve():
    try:
        serves.serve()
    except Exception as e:
        print(f"Error in serve: {e}")

def jump_set():
    try:
        jumpset.start()
    except Exception as e:
        print(f"Error in jump_set: {e}")

def jump_spike():
    try:
        jumpspike.start()
    except Exception as e:
        print(f"Error in jump_spike: {e}")

def reset():
    try:
        resets.start()
    except Exception as e:
        print(f"Error in reset: {e}")

def start_listeners():
    mouse.start()
    keyboard.start()

def start_terminal():
    terminal.start()

def command_monitor():
    while True:
        if shm.get(ShmVariable.serveCommand):
            serve()
            shm.set(ShmVariable.serveCommand, False)
        time.sleep(0.001)

def run_exe(exe_path):
    if not os.path.isfile(exe_path):
        print(f"Error: {exe_path} does not exist.")
        return None
    try:
        process = subprocess.Popen(
            exe_path,
            shell=False,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
        )
        print(f"Started \"{exe_path}\" with PID {process.pid}")
        return process
    except Exception as e:
        print(f"Error running {exe_path}: {e}")
        return None

def cleanup():
    for process in processes:
        if process:
            try:
                os.system(f"taskkill /PID {process.pid} /F")
            except Exception as e:
                print(f"Error terminating process {process.pid}: {e}")
    processes.clear()
    try:
        shm.close()
        print("Shared memory closed.")
    except Exception as e:
        print(f"Error closing shared memory: {e}")
    print("Exiting...")

atexit.register(cleanup)

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    overlay_exe = os.path.join(script_dir, "src", "overlay", "Overlay.exe")
    detection_exe = os.path.join(script_dir, "src", "detection", "Detection.exe")

    processes.append(run_exe(overlay_exe))
    processes.append(run_exe(detection_exe))

    if not any(processes):
        print("No processes started successfully. Exiting...")
        cleanup()
        exit(1)

    threads: list[threading.Thread] = []
    t_listeners = threading.Thread(target=start_listeners, daemon=True)
    threads.append(t_listeners)
    t_terminal = threading.Thread(target=start_terminal, daemon=True)
    threads.append(t_terminal)
    t_serve_monitor = threading.Thread(target=command_monitor, daemon=True)
    threads.append(t_serve_monitor)

    for t in threads:
        t.start()
    
    try:
        while True:
            # print(shm.get(ShmVariable.isServing), shm.get(ShmVariable.isToss), shm.get(ShmVariable.isServe), shm.get(ShmVariable.serveCommand), shm.get(ShmVariable.isInServeLoop), shm.get(ShmVariable.serveMode))
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("Received KeyboardInterrupt, shutting down...")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        cleanup()
        exit(0)