import threading
import datetime
import time
from queue import Queue, Empty
from utils import cleanup, init_microphone, take_command, interrupt_speech

command_queue = Queue()
listening_active = threading.Event()
is_active = False

def listen_loop():
    """Background thread for listening."""
    while listening_active.is_set():
        try:
            query = take_command().lower()
            if query != 'none':
                command_queue.put(query)
        except Exception as e:
            print(f"Listen error: {e}")
        time.sleep(0.5)

def process_command(query):
    """Process voice commands."""
    from dict_app import open_web_app, close_app,show_capabilities
    from search_now import tell_joke, get_roasted, search_youtube, google_search, check_temp
    from utils import speak
    
    # Interrupt check FIRST
    if 'stop' in query or 'quiet' in query or 'shut up' in query:
        interrupt_speech()
        return True
    
    if 'open' in query or 'launch' in query:
        open_web_app(query)
    elif 'close' in query or 'off' in query:
        close_app(query)
    elif 'capabilities' in query or 'can do' in query or 'help' in query:
        show_capabilities()
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
        speak(f"Sir the time is {datetime.datetime.now().strftime('%H:%M')}")
    elif 'sleep' in query:
        speak('Sure Sir, call me anytime')
        return False
    elif 'finally sleep' in query:
        speak('Going to sleep...')
        listening_active.clear()
        return None
    return True

def main():
    global is_active
    
    try:
        init_microphone()
        try:
            from intro import intro_screen
            intro_screen()
        except:
            pass
        
        print("JARVIS ready. Say 'wake up' to activate.\n")
        
        listening_active.set()
        threading.Thread(target=listen_loop, daemon=True).start()
        
        while listening_active.is_set():
            try:
                query = command_queue.get(timeout=0.5)
                
                if not is_active:
                    if 'wake up' in query:
                        try:
                            from greet_me import greet_me
                            greet_me()
                        except:
                            pass
                        is_active = True
                        print("JARVIS active\n")
                else:
                    result = process_command(query)
                    if result is None:
                        break
                    elif result is False:
                        is_active = False
                        print("JARVIS sleeping\n")
                        
            except Empty:
                continue
            except KeyboardInterrupt:
                print("\nShutting down...")
                listening_active.clear()
                break
                
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cleanup()
        print("JARVIS offline.")

if __name__ == "__main__":
    main()