#!/usr/bin/env python3
"""Main controller and interactive menu loop for Magic Hat framework."""

import sys
import os
from magic_hat.utils import (
    clear_screen, 
    print_tactical_header, 
    Colors, 
    load_config
)

from magic_hat.database import log_scan, get_scan_logs, get_connection

from magic_hat.remote_agent import run_remote_telemetry_agent

def main_menu():
    """Renders the primary framework interface and dispatches operational phases."""
    while True:
        clear_screen()
        print_tactical_header()
        
        print(f"{Colors.CYAN}[ OPERATIONAL PHASES & MODULES ]{Colors.ENDC}")
        print("  [1] Phase 1: Reconnaissance & Target Discovery")
        print("  [2] Phase 2: Network Mapping & Port Enumeration")
        print("  [3] Phase 3: Vulnerability & Service Audit Suite")
        print("  [4] Phase 4: Wireless & Airspace Intelligence")
        print("  [5] Phase 5: Flask Web Dashboard Control")
        print("  [6] Phase 6: Global Target Scope Manager")
        print("  [7] Phase 7: Binary Health Diagnostics")
        print("  [8] Phase 8: Webhook / Notification Hub")
        print("  [9] Phase 9: Operator Quick-Shell Launcher")
        print(" [10] Phase 10: Scan Archives & Telemetry Logs")
        print(" [11] Phase 11: Tactical Report Generation")
        print(" [12] Phase 12: Automated Remote Telemetry Agent")
        print(" [13] Exit Framework")
        print("-" * 60)
        
        choice = input(f"{Colors.YELLOW}Select operational phase [1-13]: {Colors.ENDC}").strip()
        
        if choice == '1':
            print(f"\n{Colors.GREEN}[*] Launching Reconnaissance Module...{Colors.ENDC}")
            # Insert Phase 1 handler here
            input("\nPress Enter to continue...")
        elif choice == '2':
            print(f"\n{Colors.GREEN}[*] Launching Network Mapping Module...{Colors.ENDC}")
            # Insert Phase 2 handler here
            input("\nPress Enter to continue...")
        elif choice == '3':
            print(f"\n{Colors.GREEN}[*] Launching Vulnerability & Service Audit Suite...{Colors.ENDC}")
            # Insert Phase 3 handler here
            input("\nPress Enter to continue...")
        elif choice == '4':
            print(f"\n{Colors.GREEN}[*] Launching Wireless & Airspace Intelligence...{Colors.ENDC}")
            # Insert Phase 4 handler here
            input("\nPress Enter to continue...")
        elif choice == '5':
            print(f"\n{Colors.GREEN}[*] Toggling Flask Web Dashboard...{Colors.ENDC}")
            # Insert Phase 5 handler here
            input("\nPress Enter to continue...")
        elif choice == '6':
            print(f"\n{Colors.GREEN}[*] Opening Global Target Scope Manager...{Colors.ENDC}")
            # Insert Phase 6 handler here
            input("\nPress Enter to continue...")
        elif choice == '7':
            print(f"\n{Colors.GREEN}[*] Running Binary Health Diagnostics...{Colors.ENDC}")
            # Insert Phase 7 handler here
            input("\nPress Enter to continue...")
        elif choice == '8':
            print(f"\n{Colors.GREEN}[*] Opening Webhook & Notification Hub...{Colors.ENDC}")
            # Insert Phase 8 handler here
            input("\nPress Enter to continue...")
        elif choice == '9':
            print(f"\n{Colors.GREEN}[*] Spawning Operator Quick-Shell...{Colors.ENDC}")
            os.system("bash")
        elif choice == '10':
            print(f"\n{Colors.GREEN}[*] Opening Scan Archives & Telemetry Logs...{Colors.ENDC}")
            # Insert Phase 10 handler here
            input("\nPress Enter to continue...")
        elif choice == '11':
            print(f"\n{Colors.GREEN}[*] Generating Tactical Reports...{Colors.ENDC}")
            # Insert Phase 11 handler here
            input("\nPress Enter to continue...")
        elif choice == '12':
            run_remote_telemetry_agent()
        elif choice == '13':
            print(f"\n{Colors.CYAN}[*] Shutting down Magic Hat. Stay safe, operator.{Colors.ENDC}")
            sys.exit(0)
        else:
            print(f"\n{Colors.RED}[-] Invalid selection. Choose between 1 and 13.{Colors.ENDC}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.CYAN}[*] Interrupted by operator. Exiting...{Colors.ENDC}")
        sys.exit(0)
