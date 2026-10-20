"""Utility functions, configuration loaders, and tactical headers for Magic Hat."""


import sys
import argparse
import os
import json
import shutil
import subprocess
import urllib.request


# Global engagement target state
ACTIVE_SCOPE = {"target": None}
WEBHOOK_CONFIG = {"url": ""}
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
    """Clear terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_all_device_ips():
    """Retrieve active local network interfaces and assigned IP addresses robustly."""
    interfaces = []
    try:
        if shutil.which("ip"):
            res = subprocess.run(["ip", "addr"], capture_output=True, text=True)
            current_iface = "unknown"
            for line in res.stdout.splitlines():
                if not line.startswith(" ") and not line.startswith("\t"):
                    parts = line.split(":")
                    if len(parts) >= 2:
                        current_iface = parts[1].strip().split("@")[0]
                elif "inet " in line:
                    parts = line.strip().split()
                    for i, p in enumerate(parts):
                        if p == "inet" and i + 1 < len(parts):
                            ip_cidr = parts[i + 1]
                            if current_iface != "lo" and (current_iface, ip_cidr) not in interfaces:
                                interfaces.append((current_iface, ip_cidr))
    except Exception:
        pass

    if not interfaces:
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            if ip:
                interfaces.append(("wlan0", f"{ip}/24"))
        except Exception:
            pass

    return interfaces

def get_subnet_range(ip_cidr):
    """Derive default /24 subnet range from an IP CIDR string."""
    try:
        ip_part = ip_cidr.split("/")[0]
        octets = ip_part.split(".")
        if len(octets) == 4:
            return f"{octets[0]}.{octets[1]}.{octets[2]}.0/24"
    except Exception:
        pass
    return "192.168.1.0/24"

def print_tactical_header():
    """Render persistent tactical status bar with host IP, global scope, and indicators."""
    from magic_hat.server import is_server_running
    
    srv_status = f"{Colors.GREEN}[ONLINE]{Colors.ENDC}" if is_server_running() else f"{Colors.RED}[OFFLINE]{Colors.ENDC}"
        
    ips = get_all_device_ips()
    if ips:
        primary_iface, primary_ip_cidr = ips[0]
        host_ip_str = f"{Colors.GREEN}{primary_ip_cidr}{Colors.ENDC} ({primary_iface})"
    else:
        host_ip_str = f"{Colors.RED}Not Connected{Colors.ENDC}"

    global_target = ACTIVE_SCOPE.get("target")
    scope_str = f"{Colors.CYAN}{global_target}{Colors.ENDC}" if global_target else f"{Colors.YELLOW}None (Not Locked){Colors.ENDC}"

    print("-" * 60)
    print(f" [*] Host Device IP      : {host_ip_str}")
    print(f" [*] Global Target Scope : {scope_str}")
    print(f" [*] Local Web Dashboard : {srv_status}")
    print(f" [*] Background Pipeline : {Colors.CYAN}{PIPELINE_STATE}{Colors.ENDC}")
    print("-" * 60)

def send_notification(message):
    """Send webhook notification if configured."""
    url = WEBHOOK_CONFIG.get("url")
    if not url:
        return
    try:
        data = json.dumps({"content": f"[Magic Hat Alert] {message}"}).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        urllib.request.urlopen(req, timeout=5)
    except Exception:
        pass

def check_dependencies():
    """Verify basic startup dependencies."""
    pass

def load_config():
    """Load framework configuration."""
    pass