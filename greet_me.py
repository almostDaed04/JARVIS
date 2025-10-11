import speech_recognition as sr
import pygame
import datetime

from utils import speak

r = sr.Recognizer()

# Initialize pygame for playback
pygame.mixer.init()

    
def greet_me():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak('Good Morning Sir')
        print('Good Morning Sir')
    elif hour >= 12 and hour < 17:
        speak('Good Afternoon Sir')
        print('Good Afternoon Sir')
    else:
        speak('Good Evening Sir')
        print('Good Evening Sir')
    speak('Please tell me how can I help you!')
    print('Please tell me how can I help you!')