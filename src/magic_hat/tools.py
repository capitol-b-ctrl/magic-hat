"""Offensive security tool execution handlers and loggers for Magic Hat."""

import subprocess
import re
from magic_hat.database import log_scan, get_scan_logs, get_connection
from magic_hat.utils import BANNER_IMAGE, clear_screen, get_all_device_ips, send_webhook_notification

def parse_open_ports(nmap_output):
    """Extract open ports and services from Nmap stdout using regex."""
    open_ports = []
    pattern = re.compile(r"^(\d+/(?:tcp|udp))\s+open\s+([^\n]+)", re.MULTILINE)
    matches = pattern.findall(nmap_output)
    for port_proto, service in matches:
        open_ports.append({"port": port_proto, "service": service.strip()})
    return open_ports

def handle_nmap_menu():
    """Interactive Nmap scan selection and execution menu."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: NMAP RECON SUITE ===")
    
    ips = get_all_device_ips()
    ip_str = " | ".join([f"{iface}: {ip}" for iface, ip in ips])
    print(f"[*] Active IPs -> {ip_str}")
    print("-" * 45)
    
    target = input("Enter target (IP, hostname, or CIDR): ").strip()
    if not target:
        input("\n[-] Target cannot be empty. Press Enter to return...")
        return

    print("\nSelect Nmap Scan Profile:")
    print("1. Quick Scan (-T4 -F)")
    print("2. Top 100 Ports + Version Detection (-sV --top-ports 100)")
    print("3. Full Port Sweep [-p-] (-T4)")
    print("4. Comprehensive / Aggressive Scan (-A -T4)")
    print("5. Custom Flags")
    
    choice = input("\nSelect profile [1-5]: ").strip()
    
    flags = ["-T4", "-F"]
    if choice == "2":
        flags = ["-sV", "--top-ports", "100"]
    elif choice == "3":
        flags = ["-p-", "-T4"]
    elif choice == "4":
        flags = ["-A", "-T4"]
    elif choice == "5":
        custom = input("Enter custom nmap arguments (e.g., -p 1-1000 -sS): ").strip()
        flags = custom.split()
    
    print(f"\n[+] Conjuring Nmap scan on {target} with flags: {' '.join(flags)}...")
    print("[*] Scanning in progress...")
    
    try:
        cmd = ["nmap"] + flags + [target]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        open_ports = parse_open_ports(output)
        
        clear_screen()
        print(BANNER_IMAGE)
        print(f"=== NMAP SCAN RESULTS: {target} ===")
        print("=" * 55)
        
        if open_ports:
            print(f"[+] FOUND {len(open_ports)} OPEN PORT(S):")
            print(f"{'PORT/PROTO':<12} | {'SERVICE / VERSION'}")
            print("-" * 55)
            for p in open_ports:
                print(f"{p['port']:<12} | {p['service']}")
        else:
            print("[*] No open ports detected or target is filtering responses.")
            
        print("=" * 55)
        
        log_scan("Nmap", target, output)
        print("\n[✔] Scan results successfully logged to database.")
        
    except subprocess.CalledProcessError as e:
        error_output = e.stderr or str(e)
        print(f"\n[-] Nmap failed:\n{error_output}")
        log_scan("Nmap", target, f"ERROR: {error_output}")
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
    
    iface = input("Enter interface to sniff (e.g., wlan0, rmnet0): ").strip()
    if not iface:
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
        print("=" * 55)
        print(output)
        print("=" * 55)
        
        log_scan("Net Shark", iface, output)
        print("\n[✔] Packet capture logged to database.")
    except subprocess.CalledProcessError as e:
        error_output = e.stderr or str(e)
        print(f"\n[-] Tshark capture failed: {error_output}")
        print("[-] Note: Sniffing cellular interfaces (like rmnet0) usually requires root/NetHunter privileges.")
        log_scan("Net Shark", iface, f"ERROR: {error_output}")
    except FileNotFoundError:
        print("\n[-] Error: 'tshark' not found in path.")
        
    input("\nPress Enter to return...")


def handle_web_fuzzer():
    """Tool 3: Web Directory Fuzzer (ffuf wrapper)."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: WEB DIR FUZZER (FFUF) ===")
    print("-" * 45)
    
    url = input("Enter target URL (e.g., http://10.0.0.1/FUZZ): ").strip()
    if not url:
        input("\n[-] URL cannot be empty. Press Enter...")
        return
        
    if "FUZZ" not in url:
        print("\n[!] Note: 'FUZZ' keyword missing in URL. Appending '/FUZZ'.")
        url = url.rstrip("/") + "/FUZZ"
        
    wordlist = input("Enter wordlist path (default: common.txt or wordlist path): ").strip()
    if not wordlist:
        # Common Termux or standard wordlist fallback location
        wordlist = "/data/data/com.termux/files/usr/share/wordlists/dirb/common.txt"
        
    print(f"\n[+] Launching FFUF fuzzer against {url}...")
    
    try:
        cmd = ["ffuf", "-u", url, "-w", wordlist, "-s"] # -s for silent/clean output
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(BANNER_IMAGE)
        print("=== FFUF DISCOVERY RESULTS ===")
        print("=" * 55)
        print(output if output else "[*] Scan completed, but no standard output captured.")
        print("=" * 55)
        
        log_scan("Web Fuzzer", url, output)
        print("\n[✔] Web fuzzing results successfully logged to database.")
        
    except subprocess.CalledProcessError as e:
        error_output = e.stderr or str(e)
        print(f"\n[-] FFUF failed: {error_output}")
        log_scan("Web Fuzzer", url, f"ERROR: {error_output}")
    except FileNotFoundError:
        print("\n[-] Error: 'ffuf' binary not found. Run 'pkg install ffuf'.")
        
    input("\nPress Enter to return...")

def handle_dns_recon():
    """Tool 4: DNS Recon (dig wrapper)."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: DNS FOOTPRINTING (DIG) ===")
    print("-" * 45)
    
    domain = input("Enter target domain or hostname (e.g., example.com): ").strip()
    if not domain:
        input("\n[-] Domain cannot be empty. Press Enter...")
        return
        
    print("\nSelect Record Query Type:")
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
        print(f"=== DNS RESULTS: {domain} ===")
        print("=" * 55)
        print(output)
        print("=" * 55)
        
        log_scan("DNS Recon", domain, output)
        print("\n[✔] DNS footprint logged to database.")
        
    except subprocess.CalledProcessError as e:
        error_output = e.stderr or str(e)
        print(f"\n[-] Dig failed: {error_output}")
        log_scan("DNS Recon", domain, f"ERROR: {error_output}")
    except FileNotFoundError:
        print("\n[-] Error: 'dig' binary not found. Run 'pkg install dnsutils'.")
        
    input("\nPress Enter to return...")

def handle_tech_fingerprint():
    """Tool 5: Web Tech Fingerprinting (whatweb wrapper)."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: WEB TECH FINGERPRINT (WHATWEB) ===")
    print("-" * 45)
    
    target = input("Enter target URL or IP (e.g., http://example.com): ").strip()
    if not target:
        input("\n[-] Target cannot be empty. Press Enter...")
        return
        
    print(f"\n[+] Fingerprinting technology stack for {target}...")
    
    try:
        cmd = ["whatweb", target]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(BANNER_IMAGE)
        print(f"=== TECH STACK REPORT: {target} ===")
        print("=" * 55)
        print(output)
        print("=" * 55)
        
        log_scan("Tech Fingerprint", target, output)
        print("\n[✔] Fingerprint results logged to database.")
        
    except subprocess.CalledProcessError as e:
        error_output = e.stderr or str(e)
        print(f"\n[-] WhatWeb failed: {error_output}")
        log_scan("Tech Fingerprint", target, f"ERROR: {error_output}")
    except FileNotFoundError:
        print("\n[-] Error: 'whatweb' binary not found. Ensure it is installed in Termux.")

def handle_pentest_suite_menu():
    """Parent menu for all offensive security modules."""
    while True:
        clear_screen()
        print(BANNER_IMAGE)
        print("=== OFFENSIVE SECURITY SUITE ===")
        print("---------------------------------------------")
        print("1. Nmap Recon Suite")
        print("2. Net Shark (Packet Capture / tshark)")
        print("3. Web Directory Fuzzer (ffuf / gobuster)")
        print("4. DNS Footprinting (dig)")
        print("5. Web Tech Fingerprint (whatweb)")
        print("6. Subnet & ARP Discovery")
        print("7. Wireless & RF Footprinting")
        print("8. Hash Identifier & Audit Engine")
        print("9. Exploit Search Engine (searchsploit)")
        print("10. Credential Auditor (hydra)")
        print("11. Automated Report Generator")
        print("12. Return to Main Menu")
        print("---------------------------------------------")
        
        choice = input("Select module [1-12]: ").strip()
        
        if choice == "1":
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
            from magic_hat.reports import handle_report_menu
            handle_report_menu()
        elif choice == "12":
            break
        else:
            input("Invalid choice! Press Enter to try again...")
        
    input("\nPress Enter to return...")

def handle_view_logs():
    """Display past scan logs stored in the database and view full output."""
    while True:
        clear_screen()
        print(BANNER_IMAGE)
        print("=== PAGE: SCAN ARCHIVES (LOGS) ===")
        print("-" * 55)
        
        logs = get_scan_logs()
        if not logs:
            print("No scan logs found in the archives yet.")
            input("\nPress Enter to return to the main menu...")
            break
        else:
            print(f"{'ID':<4} | {'Tool':<16} | {'Target':<16} | {'Timestamp'}")
            print("-" * 65)
            for log in logs:
                print(f"{log.get('id', 0):<4} | {log.get('tool_name', ''):<16} | {log.get('target', ''):<16} | {log.get('timestamp', '')}")
                
            print("-" * 65)
            view_id = input("Enter log ID to view full output (or press Enter to go back): ").strip()
            
            if not view_id:
                break
                
            if view_id.isdigit():
                with get_connection() as conn:
                    cursor = conn.execute("SELECT tool_name, target, timestamp, output FROM scan_logs WHERE id = ?", (view_id,))
                    row = cursor.fetchone()
                    if row:
                        clear_screen()
                        print(BANNER_IMAGE)
                        print(f"=== LOG DETAILS [ID: {view_id}] ===")
                        print(f"[*] Tool:      {row['tool_name']}")
                        print(f"[*] Target:    {row['target']}")
                        print(f"[*] Timestamp: {row['timestamp']}")
                        print("=" * 55)
                        print(row["output"])
                        print("=" * 55)
                    else:
                        print("\n[-] Error: Log ID not found.")
                input("\nPress Enter to continue...")
            else:
                print("\n[-] Invalid input. Please enter a numeric ID.")
                input("\nPress Enter to continue...")

def handle_subnet_sweep():
    """Tool 6: Local Subnet Discovery & ARP Sweeping."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: SUBNET & ARP DISCOVERY ===")
    
    ips = get_all_device_ips()
    print("[*] Active Interface IPs:")
    for iface, ip in ips:
        print(f"    - {iface}: {ip}")
    print("-" * 45)
    
    subnet = input("Enter target CIDR or interface subnet (e.g., 192.168.1.0/24): ").strip()
    if not subnet:
        input("\n[-] Subnet cannot be empty. Press Enter...")
        return
        
    print(f"\n[+] Sweeping subnet {subnet} for live hosts...")
    
    try:
        # Try arp-scan first, fallback to nmap ping sweep if unavailable
        cmd = ["arp-scan", "--localnet"] if "/" not in subnet else ["nmap", "-sn", subnet]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(BANNER_IMAGE)
        print(f"=== LIVE HOST DISCOVERY: {subnet} ===")
        print("=" * 55)
        print(output)
        print("=" * 55)
        
        log_scan("Subnet Sweep", subnet, output)
        send_webhook_notification("Subnet Sweep Complete", f"Discovered live hosts on {subnet}")
        print("\n[✔] Sweep results logged and webhook triggered.")
        
    except subprocess.CalledProcessError as e:
        error_output = e.stderr or str(e)
        print(f"\n[-] Sweep failed: {error_output}")
        log_scan("Subnet Sweep", subnet, f"ERROR: {error_output}")
    except FileNotFoundError:
        print("\n[-] Error: 'arp-scan' or 'nmap' not found in path.")
        
    input("\nPress Enter to return...")

def handle_wireless_recon():
    """Tool 7: Wireless & RF Footprinting Wrapper."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: WIRELESS & RF FOOTPRINTING ===")
    print("-" * 45)
    print("1. List Wireless Interfaces & Status (iw dev / nmcli)")
    print("2. Scan Nearby Wi-Fi Networks (nmcli device wifi list)")
    print("3. Return")
    print("-" * 45)
    
    choice = input("Select option [1-3]: ").strip()
    if choice == "1":
        cmd = ["iw", "dev"]
    elif choice == "2":
        cmd = ["nmcli", "device", "wifi", "list"]
    else:
        return
        
    print("\n[+] Querying wireless subsystem...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(BANNER_IMAGE)
        print("=== WIRELESS RECON REPORT ===")
        print("=" * 55)
        print(output)
        print("=" * 55)
        
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
    
    hash_str = input("Enter hash string to analyze: ").strip()
    if not hash_str:
        input("\n[-] Hash cannot be empty. Press Enter...")
        return
        
    # Regex-based heuristic hash identification
    identified = []
    length = len(hash_str)
    
    if length == 32 and re.match(r"^[a-fA-F0-9]{32}$", hash_str):
        identified.append("MD5 / NTLM / MD4")
    elif length == 40 and re.match(r"^[a-fA-F0-9]{40}$", hash_str):
        identified.append("SHA-1 / MySQL5.x")
    elif length == 64 and re.match(r"^[a-fA-F0-9]{64}$", hash_str):
        identified.append("SHA-256 / WPA-PSK PMK")
    elif hash_str.startswith("$2a$") or hash_str.startswith("$2b$") or hash_str.startswith("$2y$"):
        identified.append("Bcrypt (Blowfish)")
    elif hash_str.startswith("$6$"):
        identified.append("SHA-512 Crypt (Linux)")
    else:
        identified.append("Unknown or complex hash format")
        
    clear_screen()
    print(BANNER_IMAGE)
    print("=== HASH ANALYSIS RESULTS ===")
    print("=" * 55)
    print(f"[*] Input Hash: {hash_str}")
    print(f"[*] Length:     {length} characters")
    print(f"[+] Potential Formats:")
    for fmt in identified:
        print(f"    - {fmt}")
    print("=" * 55)
    
    run_crack = input("\nWould you like to invoke hashcat against this hash? (y/N): ").strip().lower()
    if run_crack == 'y':
        mode = input("Enter hashcat mode number (e.g., 0 for MD5, 1000 for NTLM): ").strip()
        wordlist = input("Enter wordlist path: ").strip()
        
        print(f"\n[+] Launching hashcat audit...")
        try:
            # Hashcat command execution wrapper
            cmd = ["hashcat", "-m", mode, hash_str, wordlist]
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            print(result.stdout)
            log_scan("Hash Audit", hash_str, result.stdout)
        except Exception as e:
            print(f"[-] Hashcat execution failed: {e}")
            
    input("\nPress Enter to return...")

def handle_exploit_search():
    """Tool 9: Exploit Search Engine (searchsploit wrapper)."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: EXPLOIT SEARCH ENGINE ===")
    print("-" * 45)
    
    query = input("Enter service or software version (e.g., 'apache 2.4', 'vsftpd 2.3.4'): ").strip()
    if not query:
        return
        
    print(f"\n[+] Querying local exploit database for '{query}'...")
    try:
        cmd = ["searchsploit", query]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(BANNER_IMAGE)
        print(f"=== EXPLOIT RESULTS: {query} ===")
        print("=" * 55)
        print(output)
        print("=" * 55)
        
        log_scan("Exploit Search", query, output)
        print("\n[✔] Exploit search results logged to database.")
    except FileNotFoundError:
        print("\n[-] Error: 'searchsploit' binary not found.")
        print("    Run 'pkg install exploitdb' or access via your Kali NetHunter chroot.")
    except Exception as e:
        print(f"[-] Searchsploit failed: {e}")
        
    input("\nPress Enter to return...")

def handle_hydra_audit():
    """Tool 10: Credential & Service Auditor (hydra wrapper)."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: CREDENTIAL AUDITOR (HYDRA) ===")
    print("-" * 45)
    
    target = input("Enter target IP/hostname: ").strip()
    service = input("Enter service protocol (ssh, ftp, http-post-form): ").strip()
    user = input("Enter username or user file path: ").strip()
    wordlist = input("Enter password wordlist path: ").strip()
    
    if not all([target, service, user, wordlist]):
        input("\n[-] All fields are required. Press Enter...")
        return
        
    print(f"\n[+] Launching Hydra brute-force audit against {target} ({service})...")
    try:
        cmd = ["hydra", "-l", user, "-P", wordlist, target, service]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print(BANNER_IMAGE)
        print("=== HYDRA AUDIT RESULTS ===")
        print("=" * 55)
        print(output)
        print("=" * 55)
        
        log_scan("Hydra Audit", f"{service}://{target}", output)
        print("\n[✔] Credential audit logged to database.")
    except Exception as e:
        print(f"[-] Hydra execution failed: {e}")
        
    input("\nPress Enter to return...")

def handle_wireless_bt_scanner():
    """Option 1: Scan nearby Wi-Fi networks and Bluetooth devices using Termux API or binaries."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== OPTION 1: WIRELESS & BLUETOOTH AIRSPACE SCAN ===")
    print("-" * 55)
    
    print("[*] Scanning nearby Wi-Fi access points...")
    wifi_output = ""
    
    # Try Termux API first (best for non-rooted Android/Termux)
    try:
        res = subprocess.run(["termux-wifi-scaninfo"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0 and res.stdout.strip() and "[]" not in res.stdout:
            wifi_output = res.stdout
    except Exception:
        pass
        
    # Fallback to nmcli or iw if Termux API isn't configured
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
        print("[-] Wi-Fi scan returned no data. (Tip: Install 'termux-api' package & app, or run in NetHunter root mode).")

    print("\n" + "=" * 55)
    print("[*] Scanning nearby Bluetooth devices...")
    bt_output = ""
    
    # Try Termux Bluetooth API
    try:
        res = subprocess.run(["termux-bluetooth-devices"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0 and res.stdout.strip() and "[]" not in res.stdout:
            bt_output = res.stdout
    except Exception:
        pass
        
    # Fallback to hcitool if available
    if not bt_output:
        try:
            res = subprocess.run(["hcitool", "scan"], capture_output=True, text=True, timeout=6)
            bt_output = res.stdout
        except Exception:
            pass
            
    if bt_output.strip():
        print(bt_output)
    else:
        print("[-] Bluetooth scan returned no data. Ensure Bluetooth is enabled and Termux:API is installed.")
        
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
        # Extract subnet from first detected IP CIDR
        _, ip_cidr = ips[0]
        default_subnet = get_subnet_range(ip_cidr)
            subnet = input(f"Enter subnet/CIDR to sweep [default {default_subnet}] (or 'b' to back): ").strip()
    if subnet.lower() in ["b", "99", "back"]:
        return
        
    target_subnet = subnet if subnet else default_subnet
    
    print(f"\n[+] Executing active ping/ARP sweep on host space: {target_subnet}...")
    print("[*] Please wait while active hosts respond...\n")
    
    try:
        cmd = ["nmap", "-sn", target_subnet]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(res.stdout)
        log_scan("Subnet Sweep", target_subnet, res.stdout)
    except Exception as e:
        print(f"[-] Subnet sweep failed: {e}")
        
    input("\nPress Enter to return to main menu...")

