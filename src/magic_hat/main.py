"""Main entry point and interactive menu layout for Magic Hat."""
import sys
import argparse
import subprocess
from magic_hat.utils import BANNER_IMAGE, clear_screen, get_all_device_ips, get_subnet_range
from magic_hat.tools import (
    handle_pentest_suite_menu, 
    handle_view_logs, 
    handle_wireless_bt_scanner, 
    handle_subnet_sweep_tool
)
from magic_hat.pipeline import run_autopilot_pipeline
from magic_hat.server import toggle_web_server, is_server_running

"""Main entry point and interactive menu layout for Magic Hat."""
from magic_hat.tools import (
    handle_pentest_suite_menu, 
    handle_view_logs, 
    handle_wireless_bt_scanner, 
    handle_subnet_sweep_tool,
    parse_open_ports
)
from magic_hat.pipeline import run_autopilot_pipeline
from magic_hat.server import toggle_web_server, is_server_running


def run_headless_recon(target_subnet):
    """Execute automated reconnaissance in headless mode without UI."""
    print(BANNER_IMAGE)
    print(f"[!] Running Magic Hat in HEADLESS mode against target space: {target_subnet}")
    print("[+] Initiating automated subnet sweep...")
    try:
        cmd = ["nmap", "-sn", target_subnet]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(res.stdout)
        from magic_hat.database import log_scan
        log_scan("Headless Subnet Sweep", target_subnet, res.stdout)
        print("[✔] Headless scan complete and logged to database.")
    except Exception as e:
        print(f"[-] Headless sweep failed: {e}")

def main():
    """Main application loop with command-line flag handling."""
    parser = argparse.ArgumentParser(description="Magic Hat Tactical Red-Team Framework")
    parser.add_argument("--headless", action="store_true", help="Run in headless automation mode")
    parser.add_argument("--target", type=str, help="Target IP or CIDR subnet for headless execution")
    parser.add_argument("--check-deps", action="store_true", help="Verify required system binaries and exit")
    args = parser.parse_args()

    if args.check_deps:
        clear_screen()
        print(BANNER_IMAGE)
        check_dependencies()
        sys.exit(0)

    if args.headless:
        config = load_config()
        target = args.target or config.get("default_subnet", "192.168.1.0/24")
        run_headless_recon(target)
        sys.exit(0)

    # Interactive Tactical Menu Loop
    while True:
        clear_screen()
        print(BANNER_IMAGE)
        
        ips = get_all_device_ips()
        print("[*] Active Interfaces & Host Spaces:")
        for iface, ip_cidr in ips:
            subnet = get_subnet_range(ip_cidr)
            print(f"    - IP: {ip_cidr} | Subnet Space: {subnet}")
        
        srv_status = "[ONLINE]" if is_server_running() else "[OFFLINE]"
        
        print("---------------------------------------------")
        print("TACTICAL OPERATIONS MENU")
        print("---------------------------------------------")
        print("1. Wireless & Bluetooth Airspace Scanner")
        print("2. Whole Subnet Host Sweep (Active Discovery)")
        print("3. Offensive Security Suite (10-Tool Suite)")
        print("4. Auto-Pilot Recon Pipeline")
        print(f"5. Toggle Local Web Dashboard {srv_status}")
        print("6. View Scan Archives (Logs)")
        print("7. Exit")
        print("---------------------------------------------")
        
        choice = input("Select an option [1-7, or 99/b]: ").strip().lower()
        
        if choice == "1":
            handle_wireless_bt_scanner()
        elif choice == "2":
            handle_subnet_sweep_tool()
        elif choice == "3":
            handle_pentest_suite_menu()
        elif choice == "4":
            run_autopilot_pipeline()
        elif choice == "5":
            toggle_web_server()
        elif choice == "6":
            handle_view_logs()
        elif choice in ["7", "99", "b", "exit"]:
            if is_server_running():
                toggle_web_server()
            clear_screen()
            print("Exiting Magic Hat. Farewell, magician!\n")
            sys.exit(0)
        else:
            input("Invalid selection! Press Enter to try again...")

if __name__ == "__main__":
    main()