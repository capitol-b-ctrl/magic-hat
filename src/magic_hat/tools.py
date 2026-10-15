"""Nmap penetration testing wrapper and logger for Magic Hat."""

import subprocess
from magic_hat.database import log_scan, get_scan_logs
from magic_hat.utils import BANNER_IMAGE, clear_screen, get_all_device_ips



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
    print("2. Service / Version Detection (-sV)")
    print("3. Comprehensive / Aggressive Scan (-A -T4)")
    print("4. Custom Flags")
    
    choice = input("\nSelect profile [1-4]: ").strip()
    
    flags = ["-T4", "-F"] # Default quick
    if choice == "2":
        flags = ["-sV"]
    elif choice == "3":
        flags = ["-A", "-T4"]
    elif choice == "4":
        custom = input("Enter custom nmap arguments (e.g., -p 22,80 -sS): ").strip()
        flags = custom.split()
    
    print(f"\n[+] Conjuring Nmap scan on {target} with arguments: {' '.join(flags)}...")
    
    try:
        cmd = ["nmap"] + flags + [target]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        print("\n" + "=" * 50)
        print(output)
        print("=" * 50)
        
        # Save output to SQLite database
        log_scan("Nmap", target, output)
        print("\n[✔] Scan results successfully logged to database.")
        
    except subprocess.CalledProcessError as e:
        error_output = e.stderr or str(e)
        print(f"\n[-] Nmap execution failed:\n{error_output}")
        log_scan("Nmap", target, f"ERROR: {error_output}")
    except FileNotFoundError:
        print("\n[-] Error: 'nmap' binary not found in your PATH.")
        print("    Run 'pkg install nmap' in Termux if it's missing.")
    
    input("\nPress Enter to return to the menu...")

def handle_view_logs():
    """Display past scan logs stored in the database."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: SCAN ARCHIVES (LOGS) ===")
    print("-" * 45)
    
    logs = get_scan_logs()
    if not logs:
        print("No scan logs found in the archives yet.")
    else:
        print(f"{'ID':<4} | {'Tool':<6} | {'Target':<18} | {'Timestamp'}")
        print("-" * 55)
        for log in logs:
            print(f"{log.get('id', 0):<4} | {log.get('tool_name', ''):<6} | {log.get('target', ''):<18} | {log.get('timestamp', '')}")
            
        view_id = input("\nEnter log ID to view full output (or press Enter to go back): ").strip()
        if view_id.isdigit():
            from magic_hat.database import get_connection
            with get_connection() as conn:
                cursor = conn.execute("SELECT output FROM scan_logs WHERE id = ?", (view_id,))
                row = cursor.fetchone()
                if row:
                    print("\n" + "=" * 50)
                    print(row["output"])
                    print("=" * 50)
                else:
                    print("[-] Log ID not found.")
            input("\nPress Enter to continue...")






