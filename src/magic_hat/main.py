"""Main lifecycle runner and menu controller for Magic Hat."""

import sys
import argparse
from magic_hat.utils import (
    BANNER_IMAGE, clear_screen, get_all_device_ips, 
    get_subnet_range, check_dependencies, load_config, 
    print_tactical_header, Colors
)
import magic_hat.utils as utils
from magic_hat.tools import (
    display_offensive_suite,
    handle_wireless_bt_scanner,
    handle_subnet_sweep_tool,
    handle_view_logs,
    handle_global_target_manager,
    handle_binary_diagnostics,
    handle_webhook_config,
    handle_quick_shell
)
from magic_hat.pipeline import run_autopilot_pipeline
from magic_hat.server import toggle_web_server, is_server_running
from magic_hat.reports import handle_report_menu

def main():
    """Main framework lifecycle loop."""
    check_dependencies()
    
    while True:
        clear_screen()
        print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
        print_tactical_header()
        
        print(f"{Colors.YELLOW}{Colors.HEADER}=== MAIN MENU ==={Colors.ENDC}".center(68))
        print("-" * 60)
        print(f"{Colors.BOLD}1.{Colors.ENDC} Phase 1: Scope & Airspace Recon (Wi-Fi/BT)")
        print(f"{Colors.BOLD}2.{Colors.ENDC} Phase 2: Active Network Discovery & Sweeping")
        print(f"{Colors.BOLD}3.{Colors.ENDC} Phase 3: Vulnerability & Service Audit Suite")
        print(f"{Colors.BOLD}4.{Colors.ENDC} Phase 4: Auto-Pilot Assessment Pipeline")
        print(f"{Colors.BOLD}5.{Colors.ENDC} Phase 5: Telemetry Server & Web Dashboard Toggle")
        print(f"{Colors.BOLD}6.{Colors.ENDC} Phase 6: Global Target Scope Manager")
        print(f"{Colors.BOLD}7.{Colors.ENDC} Phase 7: Tactical Binary Health & Diagnostics")
        print(f"{Colors.BOLD}8.{Colors.ENDC} Phase 8: Webhook & Notification Hub")
        print(f"{Colors.BOLD}9.{Colors.ENDC} Phase 9: Operator Quick-Shell Launcher")
        print(f"{Colors.BOLD}10.{Colors.ENDC} Phase 10: Scan Archives & Telemetry Logs")
        print(f"{Colors.BOLD}11.{Colors.ENDC} Phase 11: Engagement Reports & Database Management")
        print(f"{Colors.RED}12. Exit Framework{Colors.ENDC}")
        print("-" * 60)
        
        choice = input(f"{Colors.YELLOW}Select lifecycle phase [1-12, or 99/b]: {Colors.ENDC}").strip().lower()
        
        if choice in ["12", "99", "b", "exit", "quit"]:
            print(f"\n{Colors.GREEN}[*] Shutting down Magic Hat. Stay secure.{Colors.ENDC}")
            sys.exit(0)
        elif choice == "1":
            handle_wireless_bt_scanner()
        elif choice == "2":
            handle_subnet_sweep_tool()
        elif choice == "3":
            display_offensive_suite()
        elif choice == "4":
            run_autopilot_pipeline()
        elif choice == "5":
            toggle_web_server()
        elif choice == "6":
            handle_global_target_manager()
        elif choice == "7":
            handle_binary_diagnostics()
        elif choice == "8":
            handle_webhook_config()
        elif choice == "9":
            handle_quick_shell()
        elif choice == "10":
            handle_view_logs()
        elif choice == "11":
            handle_report_menu()
        else:
            input(f"{Colors.RED}Invalid lifecycle selection! Press Enter to retry...{Colors.ENDC}")

if __name__ == "__main__":
    main()
