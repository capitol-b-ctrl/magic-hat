"""Utility functions, configuration loaders, and tactical headers for Magic Hat."""

import os
import json
import shutil
import subprocess
import urllib.request

# Framework-wide Global States
PIPELINE_STATE = "READY"
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
	RADtheMAGICIAN  v0.4.0

"""

class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'    # For success messages [✔]
    YELLOW = '\033[93m'   # For warnings/notices [!]
    RED = '\033[91m'      # For errors/failures [✘]
    ENDC = '\033[0m'      # Resets color back to default
    BOLD = '\033[1m'
    DIM = '\033[2m'


def clear_screen():
    """Clear terminal screen across platforms."""
    os.system('cls' if os.name == 'nt' else 'clear')

def load_config():
    """Load configuration variables from config.json with safe defaults."""
    default_config = {
        "server_host": "127.0.0.1",
        "server_port": 8080,
        "default_wordlist": "/data/data/com.termux/files/usr/share/wordlists/dirb/common.txt",
        "webhook_url": "",
        "telegram_bot_token": "",
        "telegram_chat_id": ""
    }
    
    if os.path.exists("config.json"):
        try:
            with open("config.json", "r") as f:
                user_config = json.load(f)
                default_config.update(user_config)
        except Exception as e:
            print(f"{Colors.RED}[-] Warning: Failed to read config.json, using defaults: {e}{Colors.ENDC}")
            
    return default_config

def print_tactical_header():
    """Render persistent tactical status bar with host IP and embedded ANSI indicators."""
    from magic_hat.server import is_server_running
    
    # Server status indicator
    if is_server_running():
        srv_status = f"{Colors.GREEN}[ONLINE]{Colors.ENDC}"
    else:
        srv_status = f"{Colors.RED}[OFFLINE]{Colors.ENDC}"
        
    # Get primary host IP
    ips = get_all_device_ips()
    if ips:
        primary_iface, primary_ip_cidr = ips[0]
        host_ip_str = f"{Colors.GREEN}{primary_ip_cidr}{Colors.ENDC} ({primary_iface})"
    else:
        host_ip_str = f"{Colors.RED}Not Connected{Colors.ENDC}"

    print("-" * 60)
    print(f" [*] Host Device IP    : {host_ip_str}")
    print(f" [*] Local Web Dashboard : {srv_status}")
    print(f" [*] Background Pipeline : {Colors.CYAN}{PIPELINE_STATE}{Colors.ENDC}")
    print("-" * 60)
    
    
def get_all_device_ips():
    """Retrieve active local network interfaces and assigned IP addresses."""
    interfaces = []
    try:
        if shutil.which("ip"):
            res = subprocess.run(["ip", "-o", "-4", "addr", "show"], capture_output=True, text=True)
            for line in res.stdout.strip().split("\n"):
                parts = line.split()
                if len(parts) >= 4:
                    iface = parts[1]
                    ip_cidr = parts[3]
                    if iface != "lo":
                        interfaces.append((iface, ip_cidr))
    except Exception:
        pass
    return interfaces

def get_subnet_range(ip_cidr):
    """Compute base subnet range string from IP CIDR notation."""
    if "/" in ip_cidr:
        ip = ip_cidr.split("/")[0]
        octets = ip.split(".")
        if len(octets) == 4:
            return f"{octets[0]}.{octets[1]}.{octets[2]}.0/24"
    return "192.168.1.0/24"

def check_dependencies():
    """Verify required system utilities and display environmental readiness."""
    tools = ["nmap", "ffuf", "dig", "whatweb", "tshark", "ssh", "hydra", "pwsh", "sdptool", "l2ping"]
    print("=== ENVIRONMENT DEPENDENCY AUDIT ===".center(60))
    print("-" * 60)
    
    for tool in tools:
        found = shutil.which(tool) is not None
        status = f"{Colors.GREEN}[FOUND]{Colors.ENDC}" if found else f"{Colors.RED}[MISSING]{Colors.ENDC}"
        print(f"  * {tool:<15} : {status}")
    print("-" * 60)

def send_notification(message):
    """Dispatch status alerts to Webhook or Telegram if endpoints are configured."""
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