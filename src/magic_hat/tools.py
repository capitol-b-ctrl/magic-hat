"""Offensive security tool execution handlers and loggers for Magic Hat."""

import subprocess
import re
from magic_hat.database import log_scan, get_scan_logs, get_connection
from magic_hat.utils import BANNER_IMAGE, clear_screen, get_all_device_ips, get_subnet_range, send_webhook_notification

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
        print("=== PAGE: NMAP DEEP RECON & TARGET PROFILER ===")
        print("-" * 55)
        print("1. Quick Port Scan (-T4)")
        print("2. Service & Version Detection (-sV -T4)")
        print("3. Comprehensive Target Profile (OS, Scripts, Versions: -A -sC -T4)")
        print("4. Full Port Sweep (-p- -T4)")
        print("5. Custom Flags")
        print("99. Back to Suite Menu (b)")
        print("-" * 55)
        
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
            print(f"=== DEEP RECON REPORT: {target} ===")
            print("-" * 55)
            print(f"[*] Target OS Guess : {telemetry['os_guess']}")
            print(f"[*] MAC / Hardware  : {telemetry['mac_address']}")
            print("-" * 55)
            
            if telemetry["open_ports"]:
                print(f"{'PORT/PROTO':<12} | {'SERVICE':<15} | {'VERSION / DETAILS'}")
                print("-" * 55)
                for p in telemetry["open_ports"]:
                    print(f"{p['port']:<12} | {p['service']:<15} | {p['details']}")
            else:
                print("[*] Raw scan output (no standard ports parsed):")
                print(output[:1500])
            print("-" * 55)
            
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
    print("=== PAGE: NET SHARK (PACKET CAPTURE) ===")
    
    ips = get_all_device_ips()
    print("[*] Available Interfaces:")
    for iface, ip in ips:
        print(f"    - {iface} ({ip})")
    print("-" * 45)
    
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
    print("=== PAGE: WEB DIR FUZZER (FFUF) ===")
    print("-" * 45)
    
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
    print("=== PAGE: DNS FOOTPRINTING (DIG) ===")
    print("-" * 45)
    
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
    print("=== PAGE: WEB TECH FINGERPRINT (WHATWEB) ===")
    print("-" * 45)
    
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
    print("=== PAGE: SUBNET & ARP DISCOVERY ===")
    print("-" * 45)
    
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
    print("=== PAGE: WIRELESS & RF FOOTPRINTING ===")
    print("-" * 45)
    print("1. List Wireless Interfaces & Status (iw / nmcli)")
    print("2. Scan Nearby Wi-Fi Networks")
    print("99. Back to Suite Menu (b)")
    print("-" * 45)
    
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
    print("=== PAGE: HASH IDENTIFIER & AUDIT ===")
    print("-" * 45)
    
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
    print("=== HASH ANALYSIS RESULTS ===")
    print(f"[*] Input Hash: {hash_str}")
    print(f"[*] Length: {length} characters")
    print("[*] Potential Formats:")
    for fmt in identified:
        print(f"    - {fmt}")
    print("-" * 55)
    
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
    print("=== PAGE: EXPLOIT SEARCH ENGINE ===")
    print("-" * 45)
    
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
    print("=== PAGE: CREDENTIAL AUDITOR (HYDRA) ===")
    print("-" * 45)
    
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
    print("=== OPTION 1: WIRELESS & BLUETOOTH AIRSPACE SCAN ===")
    print("-" * 55)
    
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

    print("\n" + "=" * 55)
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
    print("=== OPTION 2: WHOLE SUBNET HOST SWEEP ===")
    print("-" * 55)
    
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

def handle_pentest_suite_menu():
    """Parent menu for all offensive & administrative auditing modules."""
    while True:
        clear_screen()
        print(BANNER_IMAGE)
        print("=== OFFENSIVE & AUDITING SECURITY SUITE ===")
        print("-" * 55)
        print("1. Nmap Recon Suite")
        print("2. Net Shark (Packet Capture / tshark)")
        print("3. Web Directory Fuzzer (ffuf)")
        print("4. DNS Footprinting (dig)")
        print("5. Web Tech Fingerprint (whatweb)")
        print("6. Subnet & ARP Discovery")
        print("7. Wireless & RF Footprinting")
        print("8. Hash Identifier & Audit Engine")
        print("9. Exploit Search Engine (searchsploit)")
        print("10. Credential Auditor (hydra)")
        print("11. SSH Auditor & Remote Command Execution")
        print("12. PowerShell Core & WinRM Auditor")
        print("13. Automated Report Generator")
        print("99. Return to Main Menu (b)")
        print("-" * 55)
        
        choice = input("Select module [1-13, or 99/b]: ").strip().lower()
        
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
            handle_subnet_sweep()
        elif choice == "7":
            handle_wireless_recon()
        elif choice == "8":
            handle_hash_identifier()
        elif choice == "9":
            handle_exploit_search()
        elif choice == "10":
            handle_hydra_audit()
        elif choice == "11":
            handle_ssh_audit()
        elif choice == "12":
            handle_powershell_audit()
        elif choice == "13":
            from magic_hat.reports import handle_report_menu
            handle_report_menu()
        else:
            input("Invalid choice! Press Enter to try again...")
            
def handle_view_logs():
    """Display past scan logs stored in the database and view full output."""
    while True:
        clear_screen()
        print(BANNER_IMAGE)
        print("=== SCAN ARCHIVES (LOGS) ===")
        print("-" * 55)
        
        logs = get_scan_logs()
        if not logs:
            print("No scan logs found in the archives yet.")
            input("\nPress Enter to return to the main menu...")
            break
            
        print(f"{'ID':<4} | {'Tool':<16} | {'Target':<15} | {'Timestamp'}")
        print("-" * 55)
        for log in logs:
            print(f"{log['id']:<4} | {log['tool_name']:<16} | {log['target']:<15} | {log['timestamp']}")
            
        print("-" * 55)
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
                    print("-" * 55)
                    print(row['output'])
                    print("-" * 55)
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
    print("=== PAGE: SSH AUDITOR & REMOTE ACCESS ===")
    print("-" * 55)
    
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
    print("=== PAGE: POWERSHELL CORE & WINRM AUDITOR ===")
    print("-" * 55)
    
    print("Select Mode:")
    print("1. Run Local PowerShell Command / One-Liner (pwsh -c)")
    print("2. WinRM Remote Query (WS-Man / Windows Hosts)")
    print("99. Back (b)")
    print("-" * 55)
    
    choice = input("Select option [1-2, or 99/b]: ").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    if choice == "1":
        ps_cmd = input("Enter PowerShell command (e.g., Get-Process, $PSVersionTable): ").strip()
        if not ps_cmd:
            return
            
        print(f"\n[+] Executing PowerShell Core command...")
        try:
            cmd = ["pwsh", "-NoProfile", "-NonInteractive", "-Command", ps_cmd]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = res.stdout
            
            clear_screen()
            print(BANNER_IMAGE)
            print("=== POWERSHELL EXECUTION OUTPUT ===")
            print(output)
            
            log_scan("PowerShell Command", "Local/Host", output)
            print("\n[✔] PowerShell telemetry logged to database.")
        except FileNotFoundError:
            print("\n[-] Error: 'pwsh' binary not found. Install PowerShell Core (`pkg install powershell` or build binary).")
        except Exception as e:
            print(f"\n[-] PowerShell execution failed: {e}")
            
    elif choice == "2":
        target = input("Enter Windows target IP/hostname: ").strip()
        user = input("Enter Domain/Local Username: ").strip()
        if not target or not user:
            return
            
        ps_script = f"Invoke-Command -ComputerName '{target}' -Credential '{user}' -ScriptBlock {{ Get-ComputerInfo }}"
        print(f"\n[+] Invoking WinRM remote assessment against {target}...")
        try:
            cmd = ["pwsh", "-NoProfile", "-Command", ps_script]
            res = subprocess.run(cmd, capture_output=True, text=True)
            print(res.stdout if res.stdout else res.stderr)
            log_scan("PowerShell WinRM Audit", target, res.stdout)
        except FileNotFoundError:
            print("\n[-] Error: 'pwsh' binary not found. Install PowerShell Core in your environment.")
        except Exception as e:
            print(f"\n[-] WinRM query failed: {e}")
            
    input("\nPress Enter to return...")
    
def handle_monitor_mode():
    """Hardware Tool: Toggle wireless interface monitor mode via airmon-ng or iwconfig."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== WIRELESS MONITOR MODE & DONGLE MANAGER ===")
    print("-" * 55)
    print("1. Check Wireless Interfaces (airmon-ng / iwconfig)")
    print("2. Enable Monitor Mode on Interface (e.g., wlan0)")
    print("3. Disable Monitor Mode")
    print("99. Back (b)")
    print("-" * 55)
    
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
    print("=== INTEGRATED WORDLIST MANAGER ===")
    print("-" * 55)
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
    