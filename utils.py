import os
import time
import tempfile
import threading
import subprocess
import speech_recognition as sr
from gtts import gTTS

r = sr.Recognizer()
mic = None
mic_lock = threading.Lock()
speak_lock = threading.Lock()

speech_interrupt = threading.Event()
is_speaking = threading.Event()

# Initialize microphone
def init_microphone():
    global mic
    with mic_lock:
        if mic:
            return
        try:
            mic = sr.Microphone()
            with mic as source:
                r.energy_threshold = 4000
                r.dynamic_energy_threshold = True
                r.adjust_for_ambient_noise(source, duration=0.5)
            print("✅ Microphone ready")
        except Exception as e:
            print(f"❌ Mic error: {e}")
            mic = None

# Speak text aloud (interruptible)
def speak(text):
    with speak_lock:
        speech_interrupt.clear()
        is_speaking.set()

        try:
            # Split text into smaller sentences
            for sentence in text.replace('!', '.').replace('?', '.').split('.'):
                sentence = sentence.strip()
                if not sentence or speech_interrupt.is_set():
                    break

                # Generate temporary mp3
                tts = gTTS(text=sentence, lang='en', tld='ca')
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                tts.write_to_fp(tmp)
                tmp.close()

                # Try to play it
                try:
                    subprocess.run(
                        ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', tmp.name],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=15
                    )
                except Exception:
                    print("[Warning] Could not play audio")

                os.remove(tmp.name)
                if speech_interrupt.is_set():
                    break

        except Exception as e:
            print(f"[Speak error]: {e}")
        finally:
            is_speaking.clear()
            time.sleep(1)

# Stop current speech
def interrupt_speech():
    speech_interrupt.set()

# Take voice command
def take_command():
    global mic
    if mic is None:
        init_microphone()
        if mic is None:
            return 'none'

    print("🎧 Listening...")
    try:
        with mic_lock:
            with mic as source:
                r.pause_threshold = 0.8
                audio = r.listen(source, phrase_time_limit=5, timeout=8)

        print("🧠 Understanding...")
        text = r.recognize_google(audio, language='en-in')
        print(f"💬 You said: {text}\n")
        return text.lower()

    except sr.WaitTimeoutError:
        print("⏱️ Timeout\n")
    except sr.UnknownValueError:
        print("❓ Unclear\n")
    except sr.RequestError as e:
        print(f"❌ Service error: {e}\n")
    except Exception as e:
        print(f"❌ Error: {e}")
        mic = None
    return 'none'

# Cleanup placeholder
def cleanup():
    pass
