import os
import threading
import datetime
import time
import sys
from queue import Queue, Empty
from utils import cleanup,init_microphone,take_command

# Command queue for background listening
command_queue = Queue()
listening_active = threading.Event()

def listen_loop():
    """Background thread that continuously listens for commands."""
    while listening_active.is_set():
        try:
            query = take_command().lower()
            if query != 'none':
                command_queue.put(query)
        except Exception as e:
            print(f"[Listen loop error]: {e}")
            time.sleep(0.5)

def process_active_command(query):
    """Process commands when JARVIS is active (after 'wake up')."""
    # lightweight local imports so module load is cheap
    from dict_app import open_web_app, close_app
    from search_now import tell_joke, get_roasted, search_youtube, google_search, check_temp
    from utils import speak  # using this speak is OK if utils imports from here; adjust if circular
    import datetime

    if 'open' in query or 'launch' in query:
        open_web_app(query)
    elif 'close' in query or 'off' in query:
        close_app(query)
    elif 'joke' in query:
        tell_joke()
    elif 'roast' in query:
        get_roasted()
    elif 'volume up' in query:
        from keyboard_controller import volume_up
        volume_up()
    elif 'volume down' in query:
        from keyboard_controller import volume_down
        volume_down()
    elif 'youtube' in query or 'play' in query:
        search_youtube(query)
    elif 'google' in query or 'search' in query:
        google_search(query)
    elif 'temperature' in query or 'weather' in query:
        check_temp(query)
    elif 'time' in query:
        current_time = datetime.datetime.now().strftime('%H:%M')
        speak(f'Sir the time is {current_time}')
    elif 'go to sleep' in query:
        speak('Sure Sir, You can call me anytime')
        return False  # Signal to exit active mode
    elif 'finally sleep' in query:
        speak('Going to sleep...')
        listening_active.clear()
        return None  # Signal to exit program
    return True  # Continue active mode

def main():
    """Main loop that manages JARVIS states."""
    try:
        # Initialize microphone and show intro (ALL before listening starts)
        from utils import init_microphone as util_init_mic  # adapt if you keep init in utils
        from intro import intro_screen

        # If utils.init_microphone exists and you want to call that, adapt accordingly.
        # Here we call our local init_microphone
        init_microphone()     # Silent calibration
        try:
            intro_screen()    # Display full intro if available
        except Exception:
            pass

        print("JARVIS is ready. Say 'wake up' to activate.\n")
        listening_active.set()
        listen_thread = threading.Thread(target=listen_loop, daemon=True)
        listen_thread.start()

        is_active = False

        while listening_active.is_set():
            try:
                query = command_queue.get(timeout=0.5)

                if not is_active:
                    if 'wake up' in query:
                        try:
                            from greet_me import greet_me
                            greet_me()
                        except Exception:
                            pass
                        is_active = True
                        print("JARVIS is now active. Listening for commands...\n")
                else:
                    result = process_active_command(query)
                    if result is None:
                        # Exit program
                        break
                    elif result is False:
                        # Go to sleep mode
                        is_active = False
                        print("JARVIS is sleeping. Say 'wake up' to reactivate.\n")

            except Empty:
                continue
            except KeyboardInterrupt:
                print("\nShutting down JARVIS...")
                listening_active.clear()
                break
            except Exception as e:
                print(f"[Main loop error]: {e}")
                time.sleep(0.5)

    finally:
        cleanup()
        print("JARVIS offline.")

if __name__ == "__main__":
    main()