#src/magic_hat/utils.py
"""Utility functions and global constants for Magic Hat."""

import socket
import subprocess
import re
import urllib.request
import json
import os
import ipaddress
import shutil

# Global persistent state flags
WEB_SERVER_ACTIVE = False
PIPELINE_STATE = "IDLE"
BANNER_IMAGE = r"""


 .--..--..--..--..--..--..--..--..--..--..--..--..--..--..--.
/ .. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \
\ \/\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ \/ /
 \/ /`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'\/ /
 / /\   /$$      /$$                     /$$             / /\
/ /\ \ | $$$    /$$$                    |__/            / /\ \
\ \/ / | $$$$  /$$$$  /$$$$$$   /$$$$$$  /$$  /$$$$$$$  \ \/ /
 \/ /  | $$ $$/$$ $$ |____  $$ /$$__  $$| $$ /$$_____/   \/ /
 / /\  | $$  $$$| $$  /$$$$$$$| $$  \ $$| $$| $$         / /\
/ /\ \ | $$\  $ | $$ /$$__  $$| $$  | $$| $$| $$        / /\ \
\ \/ / | $$ \/  | $$|  $$$$$$$|  $$$$$$$| $$|  $$$$$$$  \ \/ /
 \/ /  |__/     |__/ \_______/ \____  $$|__/ \_______/   \/ /
 / /\                          /$$  \ $$                 / /\
/ /\ \                        |  $$$$$$/                / /\ \
\ \/ /                         \______/                 \ \/ /
 \/ /   /$$   /$$             /$$                        \/ /
 / /\  | $$  | $$            | $$                        / /\
/ /\ \ | $$  | $$  /$$$$$$  /$$$$$$                     / /\ \
\ \/ / | $$$$$$$$ |____  $$|_  $$_/                     \ \/ /
 \/ /  | $$__  $$  /$$$$$$$  | $$                        \/ /
 / /\  | $$  | $$ /$$__  $$  | $$ /$$                    / /\
/ /\ \ | $$  | $$|  $$$$$$$  |  $$$$/                   / /\ \
\ \/ / |__/  |__/ \_______/   \___/                     \ \/ /
 \/ /                                                    \/ /
 / /\.--..--..--..--..--..--..--..--..--..--..--..--..--./ /\
/ /\ \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \/\ \
\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `' /
 `--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'
	RADtheMAGICIAN  v0.1.0

"""



def clear_screen():
    """Clear terminal screen safely."""
    os.system("cls" if os.name == "nt" else "clear")

def load_config():
    """Load centralized configuration from config.json."""
    config_path = os.path.join(os.getcwd(), "config.json")
    default_config = {
        "default_subnet": "192.168.1.0/24",
        "default_wordlist": "/data/data/com.termux/files/usr/share/wordlists/dirb/common.txt",
        "server_host": "127.0.0.1",
        "server_port": 8080,
        "required_binaries": ["nmap", "tshark", "ffuf", "dig", "searchsploit"]
    }
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as f:
                return json.load(f)
        except Exception:
            return default_config
    return default_config

def clear_screen():
    """Clear terminal screen safely."""
    os.system("cls" if os.name == "nt" else "clear")

def get_all_device_ips():
    """Detect active network interfaces and their IP addresses."""
    ips = []
    try:
        import subprocess
        result = subprocess.run(["ip", "addr"], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "inet " in line and "127.0.0.1" not in line:
                parts = line.strip().split()
                for part in parts:
                    if "/" in part:
                        ips.append(("network", part))
        if not ips:
            ips.append(("default", "192.168.1.139/24"))
    except Exception:
        ips.append(("default", "192.168.1.139/24"))
    return ips

def get_subnet_range(ip_cidr):
    """Calculate the network host space/subnet from a CIDR IP string."""
    try:
        net = ipaddress.ip_network(ip_cidr, strict=False)
        return str(net)
    except Exception:
        return "192.168.1.0/24"

def check_dependencies():
    """Verify presence of core security binaries in system PATH."""
    config = load_config()
    binaries = config.get("required_binaries", ["nmap", "tshark", "ffuf", "dig", "searchsploit"])
    
    print("[*] Performing pre-flight dependency check...")
    missing = []
    for binary in binaries:
        path = shutil.which(binary)
        if path:
            print(f"    [✔] {binary:<15} -> {path}")
        else:
            print(f"    [✘] {binary:<15} -> NOT FOUND")
            missing.append(binary)
            
    if missing:
        print(f"\n[!] Warning: Missing binaries: {', '.join(missing)}")
        print("[!] Some modules may fail unless installed via 'pkg install'.")
    else:
        print("\n[✔] All core dependencies verified successfully!")
    input("\nPress Enter to continue...")

def send_webhook_notification(title, message):
    """Optional webhook notification helper."""
    pass

def print_tactical_header():
    """Print banner, active network spaces, and persistent system statuses."""
    clear_screen()
    print(BANNER_IMAGE)
    ips = get_all_device_ips()
    if ips:
        print("[*] Active Interfaces & Host Spaces:")
        for iface, ip_cidr in ips:
            subnet = get_subnet_range(ip_cidr)
            print(f"    - IP: {ip_cidr} | Subnet Space: {subnet}")
    
    srv_status = "[ONLINE]" if WEB_SERVER_ACTIVE else "[OFFLINE]"
    pipe_status = PIPELINE_STATE
    print(f"[*] Status -> Web Server: {srv_status} | Pipeline: {pipe_status}")
    print("-" * 55)
    
def send_notification(message):
    """Dispatch status notifications via Webhook or Telegram if configured."""
    config = load_config()
    webhook = config.get("webhook_url", "").strip()
    tg_token = config.get("telegram_bot_token", "").strip()
    tg_chat = config.get("telegram_chat_id", "").strip()
    
    if webhook:
        try:
            req = urllib.request.Request(
                webhook, 
                data=json.dumps({"text": message}).encode('utf-8'), 
                headers={'Content-Type': 'application/json'}
            )
            urllib.request.urlopen(req, timeout=5)
        except Exception:
            pass
            
    if tg_token and tg_chat:
        try:
            url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
            payload = json.dumps({"chat_id": tg_chat, "text": f"[MAGIC HAT] {message}"}).encode('utf-8')
            req = urllib.request.Request(url, data=payload, headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req, timeout=5)
        except Exception:
            pass