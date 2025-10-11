import os
import time
import tempfile
import threading
import subprocess
import speech_recognition as sr
from gtts import gTTS

# Global state
r = sr.Recognizer()
_mic = None
_mic_lock = threading.Lock()
_speak_lock = threading.Lock()
speech_interrupt = threading.Event()
is_speaking = threading.Event()

def init_microphone():
    """Initialize microphone at startup."""
    global _mic
    with _mic_lock:
        if _mic is not None:
            return
        try:
            _mic = sr.Microphone()
            with _mic as source:
                r.energy_threshold = 4000
                r.dynamic_energy_threshold = True
                r.adjust_for_ambient_noise(source, duration=0.5)
            print("✅ Microphone ready")
        except Exception as e:
            print(f"❌ Mic error: {e}")
            _mic = None
            raise

def speak(text):
    """Convert text to speech with interrupt capability."""
    global speech_interrupt, is_speaking
    
    is_speaking.set()  # Signal that we're speaking
    
    with _speak_lock:
        speech_interrupt.clear()
        temp_file = None
        
        try:
            # Split into sentences for interruptible speech
            sentences = text.replace('!', '.').replace('?', '.').split('.')
            sentences = [s.strip() for s in sentences if s.strip()]
            
            for sentence in sentences:
                if speech_interrupt.is_set():
                    print("⏹ Speech stopped")
                    break
                
                tts = gTTS(text=sentence, lang='en', tld='ca')
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                tts.write_to_fp(temp_file)
                temp_file.close()
                
                players = [
                    ['mpg123', '-q', temp_file.name],
                    ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', temp_file.name],
                    ['mpg321', '-q', temp_file.name],
                    ['cvlc', '--play-and-exit', '--quiet', temp_file.name],
                ]
                
                played = False
                for cmd in players:
                    try:
                        proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, 
                                               stderr=subprocess.DEVNULL, close_fds=True)
                        proc.wait(timeout=15)
                        played = True
                        break
                    except (FileNotFoundError, subprocess.TimeoutExpired):
                        try:
                            proc.kill()
                        except:
                            pass
                        continue
                    except:
                        continue
                
                if not played:
                    print("[Warning] No audio player found")
                
                # Cleanup temp file
                time.sleep(0.05)
                try:
                    if os.path.exists(temp_file.name):
                        os.unlink(temp_file.name)
                except:
                    pass
                    
        except Exception as e:
            print(f"[Speak error]: {e}")
        finally:
            if temp_file:
                try:
                    if os.path.exists(temp_file.name):
                        os.unlink(temp_file.name)
                except:
                    pass
            
            time.sleep(1.5)  # Wait for audio to finish and ambient noise to settle
            is_speaking.clear()  # Done speaking

def interrupt_speech():
    """Stop ongoing speech."""
    global speech_interrupt
    speech_interrupt.set()

def take_command():
    """Listen for voice command."""
    global _mic
    
    if _mic is None:
        try:
            init_microphone()
        except:
            return 'none'
    
    # Don't print if we're speaking
    if not is_speaking.is_set():
        print("🎧 Listening...")
    
    try:
        with _mic_lock:
            with _mic as source:
                r.pause_threshold = 0.8
                audio = r.listen(source, phrase_time_limit=5, timeout=8)
        
        if not is_speaking.is_set():
            print("🧠 Understanding...")
        text = r.recognize_google(audio, language='en-in')
        
        if not is_speaking.is_set():
            print(f"💬 You said: {text}\n")
        return text
        
    except sr.WaitTimeoutError:
        if not is_speaking.is_set():
            print("⏱️  Timeout\n")
        return 'none'
    except sr.UnknownValueError:
        if not is_speaking.is_set():
            print("❓ Unclear\n")
        return 'none'
    except sr.RequestError as e:
        if not is_speaking.is_set():
            print(f"❌ Service error: {e}\n")
        return 'none'
    except Exception as e:
        if not is_speaking.is_set():
            print(f"❌ Error: {e}")
        try:
            with _mic_lock:
                _mic = None
                init_microphone()
                print("🔁 Mic reset")
        except:
            pass
        return 'none'

def cleanup():
    """Cleanup resources."""
    pass