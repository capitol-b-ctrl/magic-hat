"""Nmap penetration testing wrapper and logger for Magic Hat."""

import subprocess
import re
from magic_hat.database import log_scan, get_scan_logs, get_connection
from magic_hat.utils import BANNER_IMAGE, clear_screen, get_all_device_ips

def parse_open_ports(nmap_output):
    """Extract open ports and services from Nmap stdout using regex."""
    open_ports = []
    # Matches lines like: 22/tcp open  ssh  or  80/tcp open  http-proxy
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
    print("[*] Scanning in progress (this may take a moment)...")
    
    try:
        cmd = ["nmap"] + flags + [target]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        # Parse out open ports for a clean summary table
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
        
        # Ask if user wants to see the full raw nmap text dump
        show_raw = input("\nWould you like to view the full raw Nmap text dump? (y/N): ").strip().lower()
        if show_raw == 'y':
            clear_screen()
            print(BANNER_IMAGE)
            print("=== RAW NMAP OUTPUT ===")
            print(output)
            print("=" * 55)
        
        # Automatically log the full output to SQLite database
        log_scan("Nmap", target, output)
        print("\n[✔] Scan results and telemetry successfully logged to database.")
        
    except subprocess.CalledProcessError as e:
        error_output = e.stderr or str(e)
        print(f"\n[-] Nmap execution failed:\n{error_output}")
        log_scan("Nmap", target, f"ERROR: {error_output}")
    except FileNotFoundError:
        print("\n[-] Error: 'nmap' binary not found in your PATH.")
        print("    Run 'pkg install nmap' in Termux if it's missing.")
    
    input("\nPress Enter to return to the menu...")

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
            print(f"{'ID':<4} | {'Tool':<6} | {'Target':<18} | {'Timestamp'}")
            print("-" * 55)
            for log in logs:
                print(f"{log.get('id', 0):<4} | {log.get('tool_name', ''):<6} | {log.get('target', ''):<18} | {log.get('timestamp', '')}")
                
            print("-" * 55)
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
                        
                        # Show parsed summary or raw
                        ports = parse_open_ports(row["output"])
                        if ports:
                            print(f"[+] EXTRACTED OPEN PORTS ({len(ports)}):")
                            for p in ports:
                                print(f"    - {p['port']}: {p['service']}")
                            print("-" * 55)
                            
                        print(row["output"])
                        print("=" * 55)
                    else:
                        print("\n[-] Error: Log ID not found.")
                input("\nPress Enter to continue...")
            else:
                print("\n[-] Invalid input. Please enter a numeric ID.")
                input("\nPress Enter to continue...")
                
                
