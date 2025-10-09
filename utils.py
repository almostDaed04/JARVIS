import os
import time
import tempfile
import threading
import subprocess
from queue import Queue, Empty
import datetime

import speech_recognition as sr
from gtts import gTTS

# ---------------------------
# Global state & locks
# ---------------------------
r = sr.Recognizer()
_mic = None
_mic_lock = threading.Lock()
_speak_lock = threading.Lock()

# ---------------------------
# Microphone initialization
# ---------------------------
def init_microphone():
    """Initialize and calibrate microphone once at startup (silently)."""
    global _mic
    with _mic_lock:
        if _mic is not None:
            return  # already done
        try:
            # Use default device/sample rate to avoid PortAudio/ALSA mismatches
            _mic = sr.Microphone()  
            with _mic as source:
                # Conservative energy threshold to reduce false triggers
                r.energy_threshold = 4000
                r.dynamic_energy_threshold = True
                # Short calibration to avoid ALSA timeouts
                r.adjust_for_ambient_noise(source, duration=0.5)
            print("✅ Microphone initialized")
        except Exception as e:
            # Re-raise but include helpful text
            print(f"❌ Microphone initialization error: {e}")
            _mic = None
            raise

# ---------------------------
# Speak (gTTS -> player) with safe subprocess handling
# ---------------------------
def speak(text):
    """
    Convert text -> mp3 (gTTS) and play, ensuring the player finishes before deleting file.
    Uses mpg123 / ffplay / mpg321 / vlc in order of preference.
    """
    with _speak_lock:
        temp_file = None
        try:
            tts = gTTS(text=text, lang='en', tld='ca')
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            tts.write_to_fp(temp_file)
            temp_file.close()

            # candidate players; ffplay includes -autoexit but ffplay may return earlier on some systems,
            # so we use Popen and wait() to ensure OS file handle is released.
            players = [
                ['mpg123', '-q', temp_file.name],
                ['ffplay', '-nodisp', '-autoexit', '-loglevel', 'quiet', temp_file.name],
                ['mpg321', '-q', temp_file.name],
                ['cvlc', '--play-and-exit', '--quiet', temp_file.name],
            ]

            played = False
            for cmd in players:
                try:
                    # Use Popen so we can be absolutely sure the process completes before deleting file
                    proc = subprocess.Popen(
                        cmd,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        close_fds=True
                    )
                    # wait with a reasonable timeout to avoid blocking forever on buggy players
                    proc.wait(timeout=15)
                    played = True
                    break
                except FileNotFoundError:
                    # player not installed -> try next
                    continue
                except subprocess.TimeoutExpired:
                    try:
                        proc.kill()
                    except Exception:
                        pass
                    continue
                except Exception:
                    # fallback to trying next player
                    continue

            if not played:
                print("[Warning] No audio player found. Install one, e.g.: sudo apt-get install mpg123")
        except Exception as e:
            print(f"[Error in speak]: {e}")
        finally:
            # give OS a tiny moment to release file handles, then delete
            if temp_file:
                time.sleep(0.05)
                try:
                    if os.path.exists(temp_file.name):
                        os.unlink(temp_file.name)
                except Exception:
                    pass

# ---------------------------
# Listening / recognition
# ---------------------------
def take_command():
    """
    Listen for a voice command quickly (no repeated calibration).
    Returns recognized text or 'None' string on failure (to match your existing checks).
    """
    global _mic
    # Ensure microphone is initialized
    if _mic is None:
        try:
            init_microphone()
        except Exception as e:
            print("❌ Unable to initialize microphone for take_command():", e)
            return 'None'

    print("🎧 Listening...")

    try:
        # Ensure only one thread enters the microphone context at a time
        with _mic_lock:
            with _mic as source:
                # Shorter thresholds to avoid long blocking
                r.pause_threshold = 0.8
                audio = r.listen(source, phrase_time_limit=5, timeout=8)

        print("🧠 Understanding...")
        text = r.recognize_google(audio, language='en-in')
        print(f"💬 You said: {text}\n")
        return text

    except sr.WaitTimeoutError:
        print("⏱️  Timeout - no speech detected\n")
        return 'None'
    except sr.UnknownValueError:
        print("❓ Could not understand - try again\n")
        return 'None'
    except sr.RequestError as e:
        # network / Google API issues - don't treat it as memory corruption
        print(f"❌ Recognition service error: {e}\n")
        return 'None'
    except Exception as e:
        # This catches low-level errors (e.g., PortAudio issues). Attempt to recover.
        print(f"❌ Unexpected error in take_command: {e}\nAttempting microphone reinitialization...")
        try:
            # try reinitializing microphone once (may fix PortAudio glitches)
            with _mic_lock:
                try:
                    # attempt graceful close/recreate by dropping reference and re-init
                    _mic = None
                    init_microphone()
                    print("🔁 Microphone reinitialized after error.")
                except Exception as reinit_e:
                    print("❌ Reinitialization failed:", reinit_e)
                    _mic = None
        except Exception:
            pass
        return 'None'

def cleanup():
    """Clean up resources before exit. (Left intentionally simple.)"""
    # nothing to explicitly close for subprocess approach; leave hooks here for future resources
    pass