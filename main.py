#!/usr/bin/env python3
import os
import sys
import time
import json
import random
import requests
from datetime import datetime
import threading

os.system('clear')

def banner():
    print("\033[96m" + """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    ███    ██  █████   ██       ██████  ██████   ██████      ║
║    ████   ██ ██   ██ ██      ██      ██    ██ ██    ██      ║
║    ██ ██  ██ ███████ ██      ██      ██    ██ ██    ██      ║
║    ██  ██ ██ ██   ██ ██      ██      ██    ██ ██    ██      ║
║    ██   ████ ██   ██ ███████  ██████  ██████   ██████       ║
║                                                              ║
║                     NGL BOMBER v6.0                         ║
╚══════════════════════════════════════════════════════════════╝
""" + "\033[0m")

def loading_animation(text):
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    for char in chars:
        sys.stdout.write(f"\r\033[93m{char} {text}\033[0m")
        sys.stdout.flush()
        time.sleep(0.05)
    print(f"\r\033[92m✓ {text}\033[0m" + " " * 20)

def send_message(username, message):
    url = "https://ngl.link/api/submit"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Content-Type": "application/json"
    }
    data = {"username": username, "question": message, "deviceId": f"android-{random.randint(1000000, 9999999)}"}
    try:
        r = requests.post(url, json=data, headers=headers, timeout=10)
        return r.status_code == 200
    except:
        return False

def save_log(log_entry):
    os.makedirs("data", exist_ok=True)
    logs = []
    if os.path.exists("data/logs.json"):
        with open("data/logs.json", "r") as f:
            logs = json.load(f)
    logs.append(log_entry)
    with open("data/logs.json", "w") as f:
        json.dump(logs[-50:], f, indent=2)

while True:
    os.system('clear')
    banner()
    
    print("\033[95m╔════════════════════════════════════════════════════════════════╗")
    print("║                                                                    ║")
    print("║                       \033[93m[1] START BOMBING\033[95m                         ║")
    print("║                       \033[91m[0] EXIT\033[95m                                   ║")
    print("║                                                                    ║")
    print("╚════════════════════════════════════════════════════════════════╝\033[0m")
    
    choice = input("\n\033[96m[?] SELECT: \033[0m")
    
    if choice == "1":
        os.system('clear')
        banner()
        print("\n\033[93m╔════════════════════════════════════════════════════════════════╗")
        print("║                         BOMB SETUP                                  ║")
        print("╚════════════════════════════════════════════════════════════════╝\033[0m\n")
        
        username = input("\033[96m┌──[\033[92mNGL USERNAME\033[96m]\n└──╼ \033[0m")
        
        print("\n\033[93m┌──[\033[92mENTER MESSAGES\033[93m] (type 'done' to finish)\033[0m")
        messages = []
        while True:
            msg = input("\033[96m└──╼ \033[0m")
            if msg.lower() == "done":
                break
            if msg.strip():
                messages.append(msg)
        
        count = int(input("\n\033[96m┌──[\033[92mHOW MANY MESSAGES\033[96m]\n└──╼ \033[0m"))
        delay = float(input("\n\033[96m┌──[\033[92mDELAY (seconds)\033[96m]\n└──╼ \033[0m"))
        
        loading_animation("Connecting to NGL...")
        loading_animation("Preparing bombs...")
        
        print("\n\033[92m╔════════════════════════════════════════════════════════════════╗")
        print("║                      BOMBING STARTED                               ║")
        print("╠════════════════════════════════════════════════════════════════╣")
        print("║  \033[93mTARGET:\033[92m @{}\033[0m\033[92m                                             ║".format(username))
        print("║  \033[93mMESSAGES:\033[92m {}\033[0m\033[92m                                              ║".format(len(messages)))
        print("║  \033[93mTOTAL:\033[92m {}\033[0m\033[92m                                                ║".format(count))
        print("╚════════════════════════════════════════════════════════════════╝\033[0m\n")
        
        sent = 0
        failed = 0
        start = time.time()
        
        anim = ["|", "/", "-", "\\"]
        
        try:
            for i in range(count):
                msg = random.choice(messages)
                if send_message(username, msg):
                    sent += 1
                else:
                    failed += 1
                
                elapsed = int(time.time() - start)
                remaining = count - (sent + failed)
                percent = (sent + failed) / count * 100
                
                bar_len = 40
                filled = int(bar_len * percent / 100)
                bar = "█" * filled + "░" * (bar_len - filled)
                
                sys.stdout.write(f"\r\033[96m[{bar}]\033[0m \033[93m{percent:.0f}%\033[0m | \033[92m✓ {sent}\033[0m | \033[91m✗ {failed}\033[0m | \033[94m⏱ {remaining}\033[0m")
                sys.stdout.flush()
                
                time.sleep(delay)
        except KeyboardInterrupt:
            print("\n\n\033[93m[!] INTERRUPTED!\033[0m")
        
        elapsed = int(time.time() - start)
        print("\n")
        print("\033[92m╔════════════════════════════════════════════════════════════════╗")
        print("║                      BOMBING COMPLETE                              ║")
        print("╠════════════════════════════════════════════════════════════════╣")
        print("║  \033[93m✓ SENT:\033[92m {}\033[0m\033[92m                                                    ║".format(sent))
        print("║  \033[93m✗ FAILED:\033[91m {}\033[0m\033[92m                                                 ║".format(failed))
        print("║  \033[93m⏱ TIME:\033[94m {}s\033[0m\033[92m                                                    ║".format(elapsed))
        print("╚════════════════════════════════════════════════════════════════╝\033[0m")
        
        save_log({"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "username": username, "sent": sent, "failed": failed})
        
        print("\n\033[96m[ LOGS SAVED ]\033[0m")
        print("\n\033[93m┌──[\033[92mPRESS ENTER TO CONTINUE\033[93m]\033[0m")
        input()
    
    elif choice == "0":
        os.system('clear')
        print("\n\033[96m╔════════════════════════════════════════════════════════════════╗")
        print("║                    \033[91mEXITING NGL BOMBER\033[96m                            ║")
        print("╚════════════════════════════════════════════════════════════════╝\033[0m")
        time.sleep(1)
        os.system('clear')
        sys.exit(0)
