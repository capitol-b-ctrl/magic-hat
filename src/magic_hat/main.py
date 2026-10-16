import sys
import argparse
from magic_hat.utils import BANNER_IMAGE, clear_screen, get_all_device_ips, get_subnet_range, check_dependencies, load_config, print_tactical_header
import magic_hat.utils as utils

from magic_hat.tools import (
    display_offensive_suite,
    handle_wireless_bt_scanner,
    handle_subnet_sweep_tool,
    handle_view_logs,
    handle_nmap_menu,
    handle_net_shark,
    handle_web_fuzzer,
    handle_dns_recon,
    handle_tech_fingerprint,
    handle_subnet_sweep,
    handle_wireless_recon,
    handle_hash_identifier,
    handle_exploit_search,
    handle_hydra_audit,
    handle_ssh_audit,
    handle_powershell_audit,
    handle_monitor_mode,
    handle_wordlist_manager,
    handle_bluetooth_recon,
    handle_crypto_engine,
    handle_payload_generator,
    handle_qr_exploit,
    handle_bluetooth_attacks
)
from magic_hat.pipeline import run_autopilot_pipeline
from magic_hat.server import toggle_web_server, is_server_running

def display_lifecycle_menu():
    """Display standard security auditing workflow menus."""
    print("---------------------------------------------")
    print("               MAIN MENU           ")
    print("---------------------------------------------")
    print("1. Phase 1: Scope & Airspace Recon (Wi-Fi/BT)")
    print("2. Phase 2: Active Network Discovery & Sweeping")
    print("3. Phase 3: Vulnerability & Service Audit Suite")
    print("4. Phase 4: Auto-Pilot Assessment Pipeline")
    print("5. Phase 5: Telemetry Server & Web Dashboard Toggle")
    print("6. Phase 6: Audit Archives & Report Generation")
    print("7. Exit Framework")
    print("---------------------------------------------")

def main():
    """Main application loop."""
    parser = argparse.ArgumentParser(description="Magic Hat Tactical Framework")
    parser.add_argument("--check-deps", action="store_true", help="Verify required system binaries")
    args = parser.parse_args()

    if args.check_deps:
        clear_screen()
        print(BANNER_IMAGE)
        check_dependencies()
        sys.exit(0)

    while True:
        clear_screen()
        print(BANNER_IMAGE)
        
        ips = get_all_device_ips()
        print("[*] Active Interfaces & Host Spaces:")
        for iface, ip_cidr in ips:
            subnet = get_subnet_range(ip_cidr)
            print(f"    - IP: {ip_cidr} | Subnet Space: {subnet}")
        
        srv_status = "[ONLINE]" if is_server_running() else "[OFFLINE]"
        print(f"[*] Local Web Dashboard: {srv_status}\n")
        
        print_tactical_header()
        display_lifecycle_menu()
        
        choice = input("Select lifecycle phase [1-7, or 99/b]: ").strip().lower()
        
        if choice == "1":
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
            handle_view_logs()
        elif choice in ["7", "99", "b", "exit"]:
            if is_server_running():
                toggle_web_server()
            clear_screen()
            print("Exiting Magic Hat. Operational telemetry saved.\n")
            sys.exit(0)
        else:
            input("Invalid selection! Press Enter to try again...")

if __name__ == "__main__":
    main()
    
    
