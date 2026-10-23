"""Base utilities, root verification, and targeting helpers for Magic Hat modules."""

import os
import re
import shutil
import subprocess
from magic_hat.database import get_scan_logs
from magic_hat.utils import (
    BANNER_IMAGE,
    clear_screen,
    print_tactical_header,
    get_all_device_ips,
    get_subnet_range,
    Colors
)


def is_root():
    """Check if current process has root privileges."""
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False


def check_tsu():
    """Check if 'tsu' or 'su' is available for root elevation in Termux."""
    return shutil.which("tsu") is not None or shutil.which("su") is not None


def require_root(action_name="this action"):
    """
    Verifies root privileges. Warns the operator if running unrooted in Termux
    and asks whether to attempt execution anyway.
    """
    if is_root():
        return True
    
    print(f"\n{Colors.RED}[!] PRIVILEGE WARNING: {action_name} typically requires superuser/root privileges.{Colors.ENDC}")
    if check_tsu():
        print(f"{Colors.YELLOW}[*] Root helper detected. In Termux, you can launch Magic Hat as root using: `tsu -c magic-hat`{Colors.ENDC}")
    else:
        print(f"{Colors.YELLOW}[*] Tip: Install 'tsu' (`pkg install tsu`) or run inside a rooted PRoot environment.{Colors.ENDC}")
        
    choice = input(f"{Colors.YELLOW}Attempt to proceed anyway? [y/N]: {Colors.ENDC}").strip().lower()
    return choice in ["y", "yes"]


def print_target_context(tool_title):
    """Print tactical header, active network interfaces/subnets, and page title."""
    clear_screen()
    print_tactical_header()
    
    ips = get_all_device_ips()
    print(f"{Colors.YELLOW}[*] Active Interfaces & Host Spaces:{Colors.ENDC}")
    if ips:
        for iface, ip_cidr in ips:
            subnet = get_subnet_range(ip_cidr)
            print(f"    - [{iface}] IP: {ip_cidr} | Subnet: {subnet}")
    else:
        print(f"    {Colors.RED}[!] No active network interfaces detected (Check Wi-Fi / Hotspot){Colors.ENDC}")
        
    print("-" * 60)
    print(tool_title.center(60))
    print("-" * 60)


def select_target_interactive():
    """Display recent discovered targets from the database and let user pick one."""
    logs = get_scan_logs()
    if not logs:
        print(f"{Colors.YELLOW}[!] No scan logs or targets found in database.{Colors.ENDC}")
        return None
        
    discovered_hosts = set()
    for log_entry in logs:
        if isinstance(log_entry, dict):
            target_val = log_entry.get('target')
            tool_name = log_entry.get('tool_name', '')
            output_text = log_entry.get('output', '')
        else:
            target_val = log_entry[3] if len(log_entry) > 3 else None
            tool_name = log_entry[2] if len(log_entry) > 2 else ''
            output_text = log_entry[4] if len(log_entry) > 4 else ''

        if target_val and target_val not in ["Local Airspace", "Airspace", "Local Host"]:
            discovered_hosts.add(target_val)
            
        if any(keyword in tool_name for keyword in ["Nmap", "Sweep", "Pipeline"]):
            ips = re.findall(r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b", output_text)
            for ip in ips:
                if not ip.startswith("8.8.") and ip != "255.255.255.255":
                    discovered_hosts.add(ip)

    hosts_list = sorted(list(discovered_hosts))
    if not hosts_list:
        print(f"{Colors.YELLOW}[!] No distinct host targets parsed from recent logs.{Colors.ENDC}")
        return None

    clear_screen()
    print_tactical_header()
    print("=== INTELLIGENCE TARGET SELECTOR ===".center(60))
    print("-" * 60)
    print("Discovered targets from database logs:")
    for idx, host in enumerate(hosts_list, 1):
        print(f"  {Colors.BOLD}{idx}.{Colors.ENDC} {host}")
    print(f"  {Colors.RED}0.{Colors.ENDC} Enter manually")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select target index [1-{len(hosts_list)}] or 0 for manual: {Colors.ENDC}").strip()
    if choice.isdigit():
        c_idx = int(choice)
        if 1 <= c_idx <= len(hosts_list):
            selected = hosts_list[c_idx - 1]
            print(f"{Colors.GREEN}[*] Auto-selected Target from Database: {selected}{Colors.ENDC}")
            return selected
            
    return None


def parse_open_ports(nmap_output):
    """Extract open ports and services from Nmap stdout using regex."""
    open_ports = []
    pattern = re.compile(r"^(\d+/(?:tcp|udp))\s+open\s+([^\s]+)\s*(.*)$", re.MULTILINE)
    matches = pattern.findall(nmap_output)
    for port_proto, service, desc in matches:
        open_ports.append({"port": port_proto, "service": service.strip()})
    return open_ports


def parse_nmap_deep_telemetry(nmap_output):
    """Extract open ports, services, OS hints, and MAC addresses from Nmap stdout."""
    telemetry = {
        "open_ports": [],
        "os_guess": "Unknown / Not Detected",
        "mac_address": "Unknown",
        "device_type": "Unknown"
    }
    
    port_pattern = re.compile(r"^(\d+/(?:tcp|udp))\s+open\s+([^\s]+)\s*(.*)$", re.MULTILINE)
    for port_proto, service, desc in port_pattern.findall(nmap_output):
        telemetry["open_ports"].append({"port": port_proto, "service": service.strip(), "details": desc.strip()})
        
    os_pattern = re.compile(r"OS details:\s+(.*)$", re.MULTILINE)
    os_match = os_pattern.search(nmap_output)
    if os_match:
        telemetry["os_guess"] = os_match.group(1).strip()
    else:
        running_pattern = re.compile(r"Running:\s+(.*)$", re.MULTILINE)
        running_match = running_pattern.search(nmap_output)
        if running_match:
            telemetry["os_guess"] = running_match.group(1).strip()

    mac_pattern = re.compile(r"MAC Address:\s+([0-9A-Fa-f:]+\s+\([^)]+\))", re.MULTILINE)
    mac_match = mac_pattern.search(nmap_output)
    if mac_match:
        telemetry["mac_address"] = mac_match.group(1).strip()
        
    return telemetry
