import threading
import time
import os
import sys
from utils import speak

def loading_animation(stop_event, message="Initializing JARVIS"):
    """Display loading animation until stop_event is set."""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    idx = 0
    while not stop_event.is_set():
        sys.stdout.write(f"\r{frames[idx]} {message}...")
        sys.stdout.flush()
        idx = (idx + 1) % len(frames)
        time.sleep(0.1)
    sys.stdout.write("\r" + " " * 50 + "\r")  # Clear the line
    sys.stdout.flush()

def intro_screen():
    """Display intro animation - blocks until complete."""
    os.system("cls" if os.name == "nt" else "clear")
    
    # Show loading animation while mic calibrates (takes ~1 second)
    stop_loading = threading.Event()
    loading_thread = threading.Thread(target=loading_animation, args=(stop_loading, "Initializing JARVIS"), daemon=True)
    loading_thread.start()
    
    # Simulate initialization time (mic is already calibrated by now, but add dramatic pause)
    time.sleep(1.5)
    
    # Stop loading animation
    stop_loading.set()
    loading_thread.join()
    
    # Clear screen and show intro
    os.system("cls" if os.name == "nt" else "clear")
    
    intro = """
     ██╗ █████╗ ██████╗ ██╗   ██╗██╗███████╗
     ██║██╔══██╗██╔══██╗██║   ██║██║██╔════╝
     ██║███████║██████╔╝██║   ██║██║███████╗
██   ██║██╔══██║██╔══██╗╚██╗ ██╔╝██║╚════██║
╚█████╔╝██║  ██║██║  ██║ ╚████╔╝ ██║███████║
 ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝                                                                                                                                    
                                                           
 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 ░ J.A.R.V.I.S. - Just A Rather Very Intelligent System ░
 ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
 YOUR PERSONAL AI ASSISTANT
 """
    
    # Print intro with animation
    for line in intro.splitlines():
        print(line)
        time.sleep(0.08)
    
    print("\n ✓ JARVIS is now online \n")
    
    # Speak welcome message (blocking)
    speak('JARVIS is online. Waiting for your command sir.')
    
    # Give user time to read before listening messages start
    print("\n" + "="*50)
    time.sleep(1.0)