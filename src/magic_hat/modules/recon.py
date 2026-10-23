"""Reconnaissance, network mapping, and port profiling modules for Magic Hat."""

import subprocess
import shutil
from magic_hat.database import log_scan_result
from magic_hat.utils import (
    BANNER_IMAGE,
    clear_screen,
    print_tactical_header,
    get_all_device_ips,
    get_subnet_range,
    send_notification,
    tactical_spinner,
    Colors
)
from magic_hat.modules.base import (
    print_target_context,
    select_target_interactive,
    parse_nmap_deep_telemetry,
    require_root
)


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
        try:
            cmd = ["nmap"] + flags + [target]
            with tactical_spinner(f"Engaging Nmap profile on {target}..."):
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            output = result.stdout
            
            telemetry = parse_nmap_deep_telemetry(output)
            
            clear_screen()
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
            
            log_scan_result("Nmap Deep Recon", target, output, metadata=telemetry)
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
    
    # Check root capability for raw packet capture
    if not require_root("Packet capture / promiscuous sniffing on mobile interfaces"):
        return
        
    count = input(f"{Colors.YELLOW}Enter packet count limit (default 20): {Colors.ENDC}").strip() or "20"
    
    print(f"{Colors.GREEN}\n[+] Initializing Net Shark on {iface} (capturing {count} packets)...{Colors.ENDC}")
    print(f"{Colors.YELLOW}[*] Press Ctrl+C if you need to abort early.\n{Colors.ENDC}")
    try:
        cmd = ["tshark", "-i", iface, "-c", str(count)]
        with tactical_spinner(f"Sniffing {count} packets on interface {iface}..."):
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print_tactical_header()
        print(f"=== PACKET CAPTURE RESULTS: {iface} ===".center(60))
        print(output)
        
        log_scan_result("Net Shark", iface, output)
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
        
    print(f"{Colors.GREEN}[*] Target URL Locked: {url}{Colors.ENDC}")
    wordlist = input(f"{Colors.YELLOW}Enter wordlist path (press Enter for default): {Colors.ENDC}").strip()
    if not wordlist:
        wordlist = "/data/data/com.termux/files/usr/share/wordlists/dirb/common.txt"
        
    print(f"{Colors.GREEN}\n[+] Launching FFUF fuzzer against {url}...{Colors.ENDC}")
    try:
        cmd = ["ffuf", "-u", url, "-w", wordlist, "-s"]
        with tactical_spinner(f"Fuzzing web endpoints on {url}..."):
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print_tactical_header()
        print(f"=== FFUF DISCOVERY RESULTS ===".center(60))
        print(output if output else f"{Colors.YELLOW}[*] Scan completed, but no standard output captured.{Colors.ENDC}")
        
        log_scan_result("Web Fuzzer", url, output)
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
            
        with tactical_spinner(f"Querying DNS records for {domain}..."):
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print_tactical_header()
        print(f"=== DNS RESULTS ({domain}) ===".center(60))
        print(output)
        
        log_scan_result("DNS Recon", domain, output)
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
        with tactical_spinner(f"Fingerprinting technology stack on {target}..."):
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print_tactical_header()
        print(f"=== TECH STACK REPORT: {target} ===".center(60))
        print(output)
        
        log_scan_result("Tech Fingerprint", target, output)
        print(f"{Colors.GREEN}\n[✔] Fingerprint results logged to database.{Colors.ENDC}")
    except subprocess.CalledProcessError as e:
        print(f"{Colors.RED}\n[-] WhatWeb failed: {e.stderr or str(e)}{Colors.ENDC}")
    except FileNotFoundError:
        print(f"{Colors.RED}\n[-] Error: 'whatweb' binary not found. Ensure it is installed in Termux.{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")


def handle_subnet_sweep():
    """Phase 2: Local Subnet Discovery & Active ARP/Ping Sweeping."""
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
        with tactical_spinner(f"Sweeping subnet {target_sub} for active hosts..."):
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print_tactical_header()
        print(f"=== LIVE HOST DISCOVERY: {target_sub} ===".center(60))
        print(output)
        
        log_scan_result("Subnet Sweep", target_sub, output)
        send_notification(f"Subnet Sweep Complete: Discovered live hosts on {target_sub}")
        print(f"{Colors.GREEN}\n[✔] Sweep results logged and notification triggered.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}\n[-] Sweep failed: {e}{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")
