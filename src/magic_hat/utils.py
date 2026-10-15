#src/magic_hat/utils.py
"""Utility functions and global constants for Magic Hat."""

import socket
import subprocess
import re
import urllib.request
import json
import os

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
    """Clears the terminal screen, scrollback buffer, and resets cursor to top."""
    print("\033[2J\033[3J\033[H", end="")


def get_all_device_ips():
    """Retrieve all active network interfaces and their IP addresses on Android/Termux."""
    interfaces = []
    try:
        # Run 'ip addr' to list all interfaces and addresses
        result = subprocess.run(["ip", "addr"], capture_output=True, text=True, check=True)
        output = result.stdout
        
        current_iface = "unknown"
        for line in output.splitlines():
            # Match interface name header (e.g., "3: wlan0: <...>")
            iface_match = re.match(r"^\d+:\s+([@\w\-_]+):", line)
            if iface_match:
                current_iface = iface_match.group(1)
            
            # Match IPv4 inet address line
            inet_match = re.search(r"inet\s+([\d\.]+)(?:/\d+)?", line)
            if inet_match and current_iface != "lo":
                ip_addr = inet_match.group(1)
                interfaces.append((current_iface, ip_addr))
                
    except Exception:
        # Fallback if 'ip' command is unavailable
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            interfaces.append(("default", s.getsockname()[0]))
            s.close()
        except Exception:
            interfaces.append(("unknown", "127.0.0.1"))
            
    return interfaces

# Optional config file for webhooks
WEBHOOK_CONFIG_PATH = os.path.expanduser("~/.magic_hat_webhook.json")

def send_webhook_notification(title, message):
    """Send a notification payload to a configured webhook endpoint."""
    if not os.path.exists(WEBHOOK_CONFIG_PATH):
        return
    
    try:
        with open(WEBHOOK_CONFIG_PATH, "r") as f:
            config = json.load(f)
            webhook_url = config.get("url")
            
        if not webhook_url:
            return
            
        payload = {
            "content": f"🎩 **Magic Hat Alert**\n**{title}**\n```{message}```"
        }
        
        req = urllib.request.Request(
            webhook_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        # Fail silently so local CLI execution isn't blocked by network errors
        pass