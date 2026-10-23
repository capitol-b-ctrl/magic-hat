"""Utility functions, configuration loaders, and tactical headers for Magic Hat."""


import sys
import argparse
import os
import json
import shutil
import subprocess
import urllib.request
import socket
from contextlib import contextmanager

try:
    from rich.console import Console
    from rich.progress import (
        Progress,
        SpinnerColumn,
        TextColumn,
        BarColumn,
        TaskProgressColumn,
        TimeElapsedColumn
    )
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None


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
	@Capitol-B-CTRL  v0.5.0

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

    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC} ")
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
    """Verify basic startup dependencies and return dict of status."""
    config = load_config()
    binaries = config.get("required_binaries", ["nmap", "tshark", "ffuf", "dig", "searchsploit"])
    results = {}
    for b in binaries:
        results[b] = shutil.which(b) is not None
    return results

def load_config():
    """Load framework configuration from config.json with fallback defaults."""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, "r") as cf:
                return json.load(cf)
        except Exception:
            pass
    return {
        "default_subnet": "192.168.1.0/24",
        "default_wordlist": "/data/data/com.termux/files/usr/share/wordlists/dirb/common.txt",
        "server_host": "127.0.0.1",
        "server_port": 8080,
        "required_binaries": ["nmap", "tshark", "ffuf", "dig", "searchsploit"],
        "webhook_url": ""
    }


@contextmanager
def tactical_spinner(description="Processing tactical telemetry...", spinner="dots"):
    """
    Context manager that displays a matrix-green spinner
    during long-running network or audit operations.
    """
    if RICH_AVAILABLE and console:
        with console.status(f"[bold green]{description}[/bold green]", spinner=spinner) as status:
            yield status
    else:
        print(f"\033[92m[*] {description}\033[0m")
        yield None


def create_tactical_progress():
    """
    Returns a configured Rich Progress instance with a matrix-green theme
    for tracking multi-step pipeline actions.
    """
    if RICH_AVAILABLE and console:
        return Progress(
            SpinnerColumn(spinner_name="dots", style="bold green"),
            TextColumn("[bold green]{task.description}[/bold green]"),
            BarColumn(bar_width=None, style="dim green", complete_style="bold green"),
            TaskProgressColumn(style="bold cyan"),
            TimeElapsedColumn(),
            console=console
        )
    return None
