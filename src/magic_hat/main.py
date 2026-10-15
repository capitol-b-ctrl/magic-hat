"""Main entry point and interactive menu layout for Magic Hat."""

import sys
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



def main():
    """Main tactical application loop."""
    while True:
        clear_screen()
        print(BANNER_IMAGE)
        
        # Display Network Interfaces & Subnet Host Space
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
