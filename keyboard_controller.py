import os
import subprocess
import time
import pyautogui

def volume_up():
    for i in range(6):
        os.system("amixer -D pulse sset Master 5%+")
        
def volume_down():
    for i in range(6):
        os.system("amixer -D pulse sset Master 5%-")
        
def mute():
    os.system("amixer -D pulse sset Master toggle")

def pause_and_play():
    subprocess.run(["xdotool", "search", "--onlyvisible", "--class", "firefox", "windowactivate"])
    time.sleep(0.3)
    pyautogui.click(x=700, y=400)  # coordinates inside video
    pyautogui.press('k') 
