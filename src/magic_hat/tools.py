"""Offensive security tool execution coordinator and module dispatcher for Magic Hat."""

from magic_hat.utils import BANNER_IMAGE, clear_screen, Colors
from magic_hat.modules import (
    is_root,
    check_tsu,
    require_root,
    print_target_context,
    select_target_interactive,
    parse_open_ports,
    parse_nmap_deep_telemetry,
    handle_nmap_menu,
    handle_net_shark,
    handle_web_fuzzer,
    handle_dns_recon,
    handle_tech_fingerprint,
    handle_subnet_sweep,
    handle_hydra_audit,
    handle_ssh_audit,
    handle_powershell_audit,
    handle_hash_identifier,
    handle_exploit_search,
    handle_wireless_recon,
    handle_wireless_bt_scanner,
    handle_monitor_mode,
    handle_bluetooth_recon,
    handle_bluetooth_attacks,
    handle_payload_generator,
    handle_qr_exploit,
    handle_crypto_engine,
    handle_global_target_manager,
    handle_binary_diagnostics,
    handle_webhook_config,
    handle_quick_shell,
    handle_wordlist_manager,
    handle_view_logs
)

# Backward-compatibility alias
handle_subnet_sweep_tool = handle_subnet_sweep


def display_offensive_suite():
    """Renders the offensive and tactical deployment suite menu with root capability indicators."""
    root_tag = f" {Colors.RED}[ROOT]{Colors.ENDC}" if not is_root() else ""
    
    while True:
        clear_screen()
        print(f"{Colors.YELLOW}{BANNER_IMAGE}{Colors.ENDC}")
        print(f"{Colors.YELLOW}{Colors.HEADER}=== OFFENSIVE & TACTICAL DEPLOYMENT SUITE ==={Colors.ENDC}".center(60))
        print("=" * 60)
        print(f"{Colors.YELLOW}--- RECON & PROFILING ---{Colors.ENDC}".center(60, " "))
        print("-" * 60)
        print(f"{Colors.BOLD}1.{Colors.ENDC} Recon & Target Profiler")
        print(f"{Colors.BOLD}2.{Colors.ENDC} Net Shark Packet Capture (tshark){root_tag}")
        print(f"{Colors.BOLD}3.{Colors.ENDC} Web Directory Fuzzer (ffuf)")
        print(f"{Colors.BOLD}4.{Colors.ENDC} DNS Footprinting (dig)")
        print(f"{Colors.BOLD}5.{Colors.ENDC} Web Tech Stack Fingerprinting (whatweb)")
        print(f"{Colors.BOLD}6.{Colors.ENDC} Wireless & RF Footprinting")
        print("-" * 60)
        print(f"{Colors.YELLOW}--- AUDITING & EXPLOITATION ---{Colors.ENDC}".center(60, " "))
        print("-" * 60)
        print(f"{Colors.BOLD}7.{Colors.ENDC} SSH & PowerShell Remote Auditors")
        print(f"{Colors.BOLD}8.{Colors.ENDC} Hash Identifier & Cracking Assistant")
        print(f"{Colors.BOLD}9.{Colors.ENDC} Exploit Database Search (searchsploit)")
        print(f"{Colors.BOLD}10.{Colors.ENDC} Credential Service Auditor (hydra)")
        print("-" * 60)
        print(f"{Colors.YELLOW}--- TACTICAL DEPLOYMENT & UTILS ---{Colors.ENDC}".center(60, " "))
        print("-" * 60)
        print(f"{Colors.BOLD}11.{Colors.ENDC} Cryptographic Engine (Base64/XOR)")
        print(f"{Colors.BOLD}12.{Colors.ENDC} Tactical Reverse Shell Generator")
        print(f"{Colors.BOLD}13.{Colors.ENDC} ASCII QR Code Payload Generator")
        print(f"{Colors.BOLD}14.{Colors.ENDC} Bluetooth Attack & SDP Suite{root_tag}")
        print(f"{Colors.BOLD}15.{Colors.ENDC} Wireless Monitor Mode Manager{root_tag}")
        print(f"{Colors.BOLD}16.{Colors.ENDC} Wordlist Manager")
        print("=" * 60)
        print(f"{Colors.RED}99. Back to Lifecycle Menu (b){Colors.ENDC}".center(60, " "))
        print("=" * 60)
        
        choice = input(f"{Colors.YELLOW}Select tactical module [1-16, or 99/b]: {Colors.ENDC}").strip().lower()
        if choice in ["99", "b", "back"]:
            break
        elif choice == "1":
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
            handle_wireless_recon()
        elif choice == "7":
            handle_ssh_audit()
        elif choice == "8":
            handle_hash_identifier()
        elif choice == "9":
            handle_exploit_search()
        elif choice == "10":
            handle_hydra_audit()
        elif choice == "11":
            handle_crypto_engine()
        elif choice == "12":
            handle_payload_generator()
        elif choice == "13":
            handle_qr_exploit()
        elif choice == "14":
            handle_bluetooth_attacks()
        elif choice == "15":
            handle_monitor_mode()
        elif choice == "16":
            handle_wordlist_manager()
        else:
            input(f"{Colors.RED}Invalid choice! Press Enter to try again...{Colors.ENDC}")
