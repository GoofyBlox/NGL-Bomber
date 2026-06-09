import os
import sys
import time
import json
import random
import requests
from datetime import datetime

RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
PURPLE = "\033[95m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def clear():
    os.system('clear')

def banner():
    print(BOLD + CYAN + r"""
╔═══════════════════════════════════════════════════════════════════════════════╗
║                                                                               ║
║    ███    ██  █████   ██       ██████  ██████   ██████  ███    ██            ║
║    ████   ██ ██   ██ ██      ██      ██    ██ ██    ██ ████   ██            ║
║    ██ ██  ██ ███████ ██      ██      ██    ██ ██    ██ ██ ██  ██            ║
║    ██  ██ ██ ██   ██ ██      ██      ██    ██ ██    ██ ██  ██ ██            ║
║    ██   ████ ██   ██ ███████  ██████  ██████   ██████  ██   ████            ║
║                                                                               ║
║                     NGL SPAM BOMBER v4.0 - TERMUX                            ║
╚═══════════════════════════════════════════════════════════════════════════════╝
""" + RESET)

def send_message(username, message):
    url = "https://ngl.link/api/submit"
    headers = {
        "User-Agent": random.choice([
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15"
        ]),
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "username": username,
        "question": message,
        "deviceId": f"android-{random.randint(1000000, 9999999)}"
    }
    try:
        r = requests.post(url, json=data, headers=headers, timeout=10)
        return r.status_code == 200
    except:
        return False

def load_messages():
    os.makedirs("data", exist_ok=True)
    if os.path.exists("data/saved_messages.txt"):
        with open("data/saved_messages.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def save_messages(messages):
    os.makedirs("data", exist_ok=True)
    with open("data/saved_messages.txt", "w") as f:
        for msg in messages:
            f.write(msg + "\n")

def save_log(log_entry):
    os.makedirs("data", exist_ok=True)
    logs = []
    if os.path.exists("data/spam_logs.json"):
        with open("data/spam_logs.json", "r") as f:
            logs = json.load(f)
    logs.append(log_entry)
    with open("data/spam_logs.json", "w") as f:
        json.dump(logs[-50:], f, indent=2)

def view_logs():
    if os.path.exists("data/spam_logs.json"):
        with open("data/spam_logs.json", "r") as f:
            logs = json.load(f)
        if logs:
            for log in reversed(logs[-15:]):
                print(f"[{log['timestamp']}] @{log['username']} - ✅ {log['sent']} | ❌ {log['failed']}")
        else:
            print("[-] No logs")
    else:
        print("[-] No logs")

def main():
    while True:
        clear()
        banner()
        print(PURPLE + "\n╔══════════════════════════════════════════════════════════════════════╗")
        print("║                         MAIN MENU                                            ║")
        print("╠══════════════════════════════════════════════════════════════════════╣")
        print("║  " + GREEN + "[1]" + RESET + " START SPAM BOMBER                                        ║")
        print("║  " + GREEN + "[2]" + RESET + " MANAGE MESSAGES                                         ║")
        print("║  " + GREEN + "[3]" + RESET + " VIEW LOGS                                              ║")
        print("║  " + GREEN + "[4]" + RESET + " CLEAR LOGS                                              ║")
        print("║  " + RED + "[0]" + RESET + " EXIT                                                    ║")
        print("╚══════════════════════════════════════════════════════════════════════╝" + RESET)
        
        choice = input("\n[?] Select: ")
        
        if choice == "1":
            clear()
            banner()
            username = input("\n[?] NGL Username: ")
            
            messages = load_messages()
            if not messages:
                print(YELLOW + "\n[!] No saved messages. Add some first." + RESET)
                print("\nEnter messages (type 'done' to finish):")
                while True:
                    msg = input("> ")
                    if msg.lower() == "done":
                        break
                    if msg.strip():
                        messages.append(msg)
                save_messages(messages)
            
            count = int(input("\n[?] Number of messages to send: "))
            delay = float(input("[?] Delay between messages (seconds): "))
            
            print(GREEN + f"\n[+] Spamming @{username}..." + RESET)
            print(YELLOW + "[+] Press Ctrl+C to stop\n" + RESET)
            
            sent = 0
            failed = 0
            start = time.time()
            
            try:
                for i in range(count):
                    msg = random.choice(messages)
                    if send_message(username, msg):
                        sent += 1
                    else:
                        failed += 1
                    elapsed = int(time.time() - start)
                    print(f"\r✅ Sent: {sent} | ❌ Failed: {failed} | ⏱️ {elapsed}s", end="")
                    time.sleep(delay)
            except KeyboardInterrupt:
                print(YELLOW + "\n\n[!] Stopped" + RESET)
            
            print(f"\n\n{GREEN}[+] Complete! Sent: {sent} | Failed: {failed}" + RESET)
            
            save_log({
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "username": username,
                "sent": sent,
                "failed": failed
            })
            input("\nPress Enter...")
        
        elif choice == "2":
            clear()
            banner()
            messages = load_messages()
            print(CYAN + f"\n[+] Current Messages ({len(messages)}):" + RESET)
            for i, msg in enumerate(messages, 1):
                print(f"  {i}. {msg[:50]}{'...' if len(msg) > 50 else ''}")
            
            print("\n[1] Add Messages")
            print("[2] Clear All")
            sub = input("\nSelect: ")
            
            if sub == "1":
                print(YELLOW + "\nEnter messages (type 'done' to finish):" + RESET)
                while True:
                    msg = input("> ")
                    if msg.lower() == "done":
                        break
                    if msg.strip():
                        messages.append(msg)
                save_messages(messages)
                print(GREEN + f"[+] Saved {len(messages)} messages" + RESET)
            elif sub == "2":
                confirm = input(RED + "Delete all? (y/n): " + RESET)
                if confirm.lower() == "y":
                    save_messages([])
                    print(GREEN + "[+] All messages deleted" + RESET)
            input("\nPress Enter...")
        
        elif choice == "3":
            clear()
            banner()
            view_logs()
            input("\nPress Enter...")
        
        elif choice == "4":
            if os.path.exists("data/spam_logs.json"):
                os.remove("data/spam_logs.json")
                print(GREEN + "[+] Logs cleared" + RESET)
            else:
                print(YELLOW + "[-] No logs to clear" + RESET)
            time.sleep(1)
        
        elif choice == "0":
            print(GREEN + "\n[✓] Goodbye!" + RESET)
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(YELLOW + "\n[!] Exiting..." + RESET)
        sys.exit(0)
