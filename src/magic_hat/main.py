#!/usr/bin/env python3
"""Main controller and interactive menu loop for Magic Hat framework."""

import sys

import os

from magic_hat.utils import (
    clear_screen, 
    print_tactical_header, 
    Colors, 
    load_config,
    BANNER_IMAGE
)
from magic_hat.database import (log_scan, get_scan_logs, get_connection
)
from magic_hat.reports import handle_report_menu

from magic_hat.remote_agent import run_remote_telemetry_agent

from magic_hat.tools import (
    display_offensive_suite,
    handle_subnet_sweep,
    handle_hydra_audit,
    handle_wireless_recon,
    handle_global_target_manager,
    handle_binary_diagnostics,
    handle_webhook_config,
    handle_quick_shell,
    handle_view_logs
)
from magic_hat.server import (toggle_web_server, is_server_running, log_detail
)

from magic_hat.pipeline import ( run_autopilot_pipeline, 
)

def main_menu():
    """Renders the primary framework interface and dispatches operational phases directly to their handlers."""
    while True:
        clear_screen()
        print_tactical_header()
        
        print(f"{Colors.CYAN}[ OPERATIONAL PHASES & MODULES ]{Colors.ENDC}")
        print("-" * 60  )
        print(f"  {Colors.GREEN}[1]{Colors.ENDC} Phase 1: Offensive & Tactical Deployment Suite")
        print(f"  {Colors.GREEN}[2]{Colors.ENDC} Phase 2: Network Mapping & Subnet Discovery")
        print(f"  {Colors.GREEN}[3]{Colors.ENDC} Phase 3: Vulnerability & Service Audit Suite")
        print(f"  {Colors.GREEN}[4]{Colors.ENDC} Phase 4: Wireless & Airspace Intelligence")
        print(f"  {Colors.GREEN}[5]{Colors.ENDC} Phase 5: Flask Web Dashboard Control")
        print(f"  {Colors.GREEN}[6]{Colors.ENDC} Phase 6: Global Target Scope Manager")
        print(f"  {Colors.GREEN}[7]{Colors.ENDC} Phase 7: Binary Health Diagnostics")
        print(f"  {Colors.GREEN}[8]{Colors.ENDC} Phase 8: Webhook / Notification Hub")
        print(f"  {Colors.GREEN}[9]{Colors.ENDC} Phase 9: Operator Quick-Shell Launcher")
        print(f"  {Colors.GREEN}[10]{Colors.ENDC} Phase 10: Scan Archives & Telemetry Logs")
        print(f"  {Colors.GREEN}[11]{Colors.ENDC} Phase 11: Tactical Report Generation")
        print(f"  {Colors.GREEN}[12]{Colors.ENDC} Phase 12: Automated Remote Telemetry Agent")
        print(f"{Colors.YELLOW}" + "-" * 60 + f"{Colors.ENDC}")
        print(f"  {Colors.RED}[13]{Colors.ENDC} Exit Framework")
        print(f"{Colors.YELLOW}" + "-" * 60 + f"{Colors.ENDC}")
        
        choice = input(f"{Colors.YELLOW}Select operational phase [1-13]: {Colors.ENDC}").strip()
        
        if choice == '1':
            display_offensive_suite()
        elif choice == '2':
            handle_subnet_sweep()
        elif choice == '3':
            handle_hydra_audit()
        elif choice == '4':
            handle_wireless_recon()
        elif choice == '5':
            toggle_web_server()
        elif choice == '6':
            handle_global_target_manager()
        elif choice == '7':
            handle_binary_diagnostics()
        elif choice == '8':
            handle_webhook_config()
        elif choice == '9':
            handle_quick_shell()
        elif choice == '10':
            handle_view_logs()
        elif choice == '11':
            handle_report_menu()
        elif choice == '12':
            run_remote_telemetry_agent()
        elif choice == '13':
            print(f"\n{Colors.CYAN}[*] Shutting down Magic Hat. Stay safe, operator.{Colors.ENDC}")
            sys.exit(0)
        else:
            print(f"\n{Colors.RED}[-] Invalid selection. Choose between 1 and 13.{Colors.ENDC}")
            input(f"{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")

def main():
    """Entry point wrapper called by the console script."""
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.CYAN}[*] Interrupted by operator. Exiting...{Colors.ENDC}")
        sys.exit(0)

if __name__ == "__main__":
    main()
