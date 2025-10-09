import webbrowser
from utils import speak, take_command
import os

app_list = {
    "calculator": "gnome-calculator",
    "text_editor": "gedit",
    "firefox": "firefox",
    "chrome": "google-chrome",
    "file_manager": "nautilus",
    "terminal": "gnome-terminal",
    "vlc": "vlc",
    "libreoffice_writer": "libreoffice --writer",
    "libreoffice_calc": "libreoffice --calc",
    "libreoffice_impress": "libreoffice --impress",
    "system_monitor": "gnome-system-monitor",
    "vs code": "code"
}

query = take_command().lower()

def open_web_app(query):
    speak('Launching, Sir')
    query = query.lower()
    
    for word in ['jarvis', 'open', 'search', 'launch']:
        query = query.replace(word, '')
    query = query.strip()
    
    if '.com' in query or '.org' in query or '.co.in' in query:
        if query.startswith('http://') or query.startswith('https://'):
            webbrowser.open_new(query)
        else:
            webbrowser.open_new(f'https://www.{query}')
    else:
        for app in list(app_list.keys()):
            if app in query:
                os.system(f"{app_list[app]} > /dev/null 2>&1 & disown")
            
            
def close_app(query):
    speak('Closing, Sir')
    query = query.lower()
    
    for word in ['jarvis', 'close', 'remove', 'kill','the']:
        query = query.replace(word, '')
    query = query.strip()
    
    for app in list(app_list.keys()):
        if app in query:
            os.system(f"pkill -f {app_list[app]}")
