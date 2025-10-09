import requests
from utils import speak,take_command
import webbrowser
import wikipedia as googleScrap


query = take_command().lower()

def check_temp(query):
    words = ['what','is','how','what\'s','temperature','temp','in','the','at']
    location = query
    for word in words:
        location = location.replace(word,'').strip()
    
    try:
        api_key = "cfe436c6417b3cb55504d34902225eb5"  
        url = f"https://api.openweathermap.org/data/2.5/weather?q={location},uk&APPID={api_key}"
        
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200:
            temp = data['main']['temp']
            speak(f"The temperature in {location} is {temp} degrees Celsius")
        else:
            speak("Sorry, I couldn't find weather information for that location.")
    except Exception as e:
        speak("Sorry, I could not fetch the temperature right now.")
        print(f"Error: {e}")
        
# google search
def google_search(query):
    for word in ['google','google search']:
        query = query.replace(word,'')
        query.strip()
        
    try:
        speak(f'Searching for {query} on google')
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open_new(url)
        result = googleScrap.summary(query, sentences=1, auto_suggest=False, redirect=True)
        speak(result)
    except:    
        print('There is no output to be speakable')
   
# youtube search
def search_youtube(query):
        
    for word in ['youtube','youtube search','play','on','search']:
        query = query.replace(word,'')
        
    try:
        speak(f'Searching for {query} on youtube')
        url = f"https://www.youtube.com/results?search_query={query}"
        speak('This is what I found,sir')
        webbrowser.open_new(url)  
        speak('Done,sir')
    except:
        print('There is no output to be speakable')

import pyjokes

def tell_joke():
    joke = pyjokes.get_joke()
    print(f"Jarvis: {joke}")
    speak(joke)
    
import random

def get_roasted():
    roasts = [
        "You're like a cloud. When you disappear, it's a beautiful day.",
        "You're proof that even evolution takes breaks sometimes.",
        "You have something on your chin... no, the third one down.",
        "If I wanted to kill myself, I'd climb your ego and jump to your IQ.",
        "You're like a software update. Whenever I see you, I think: 'Do I really need this right now?'",
        "You bring people so much joy… when you leave the room."
    ]
    burn = random.choice(roasts)
    print(f"Jarvis: {burn}")
    speak(burn)
