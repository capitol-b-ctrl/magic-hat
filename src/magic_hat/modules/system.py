"""System utilities, diagnostics, scope management, and log archives for Magic Hat."""

import os
import shutil
import subprocess
from magic_hat.database import get_scan_logs, get_connection
from magic_hat.utils import (
    BANNER_IMAGE,
    clear_screen,
    print_tactical_header,
    send_notification,
    ACTIVE_SCOPE,
    WEBHOOK_CONFIG,
    Colors
)
from magic_hat.modules.base import select_target_interactive, is_root, check_tsu


def handle_global_target_manager():
    """Phase 6: Global Target Scope Manager."""
    while True:
        clear_screen()
        print_tactical_header()
        print("=== GLOBAL TARGET SCOPE MANAGER ===".center(60))
        print("-" * 60)
        current = ACTIVE_SCOPE.get("target")
        print(f"[*] Currently Locked Target: {Colors.CYAN}{current if current else 'None'}{Colors.ENDC}")
        print("-" * 60)
        print(f"{Colors.BOLD}1.{Colors.ENDC} Set Global Target Manually")
        print(f"{Colors.BOLD}2.{Colors.ENDC} Select Target from Database Intelligence")
        print(f"{Colors.BOLD}3.{Colors.ENDC} Clear / Reset Global Target Scope")
        print(f"{Colors.RED}99. Back to Main Menu (b){Colors.ENDC}")
        print("-" * 60)
        
        choice = input(f"{Colors.YELLOW}Select option [1-3, or 99/b]: {Colors.ENDC}").strip().lower()
        if choice in ["99", "b", "back"]:
            break
        elif choice == "1":
            new_t = input(f"{Colors.YELLOW}Enter target IP or hostname: {Colors.ENDC}").strip()
            if new_t:
                ACTIVE_SCOPE["target"] = new_t
                print(f"{Colors.GREEN}[✔] Global target locked to: {new_t}{Colors.ENDC}")
                input(f"{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")
        elif choice == "2":
            selected = select_target_interactive()
            if selected:
                ACTIVE_SCOPE["target"] = selected
                print(f"{Colors.GREEN}[✔] Global target locked to: {selected}{Colors.ENDC}")
                input(f"{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")
        elif choice == "3":
            ACTIVE_SCOPE["target"] = None
            print(f"{Colors.YELLOW}[*] Global target scope cleared.{Colors.ENDC}")
            input(f"{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}")


def handle_binary_diagnostics():
    """Phase 7: Tactical Binary Health & Dependency Diagnostics."""
    clear_screen()
    print_tactical_header()
    print("=== BINARY HEALTH & ENVIRONMENT DIAGNOSTICS ===".center(60))
    print("-" * 60)
    
    # Root & elevation status
    root_status = f"{Colors.GREEN}YES (UID 0){Colors.ENDC}" if is_root() else f"{Colors.YELLOW}NO (Unprivileged){Colors.ENDC}"
    tsu_status = f"{Colors.GREEN}AVAILABLE{Colors.ENDC}" if check_tsu() else f"{Colors.DIM}NOT FOUND{Colors.ENDC}"
    print(f"[*] Superuser / Root Status  : {root_status}")
    print(f"[*] Termux Root Helper (tsu) : {tsu_status}")
    print("-" * 60)
    
    binaries = [
        "nmap", "tshark", "ffuf", "dig", "whatweb", 
        "hydra", "hashcat", "searchsploit", "pwsh", 
        "airmon-ng", "bluetoothctl", "sdptool", "l2ping"
    ]
    
    print(f"{'BINARY / TOOL':<18} | {'STATUS':<12} | {'PATH / NOTES'}")
    print("-" * 60)
    for b in binaries:
        path = shutil.which(b)
        if path:
            status = f"{Colors.GREEN}OPERATIONAL{Colors.ENDC}"
            note = path
        else:
            status = f"{Colors.RED}MISSING [✘]{Colors.ENDC}"
            note = "Run `pkg install ...`"
        print(f"{b:<18} | {status:<20} | {note}")
        
    print("-" * 60)
    input(f"{Colors.YELLOW}Press Enter to return to main menu...{Colors.ENDC}")


def handle_webhook_config():
    """Phase 8: Webhook & Notification Hub."""
    while True:
        clear_screen()
        print_tactical_header()
        print("=== WEBHOOK & NOTIFICATION HUB ===".center(60))
        print("-" * 60)
        curr_url = WEBHOOK_CONFIG.get("url", "")
        print(f"[*] Current Webhook URL: {Colors.CYAN}{curr_url if curr_url else 'Not Configured'}{Colors.ENDC}")
        print("-" * 60)
        print(f"{Colors.BOLD}1.{Colors.ENDC} Set / Update Webhook URL (Discord / Telegram)")
        print(f"{Colors.BOLD}2.{Colors.ENDC} Send Test Notification")
        print(f"{Colors.BOLD}3.{Colors.ENDC} Disable / Clear Webhook")
        print(f"{Colors.RED}99. Back to Main Menu (b){Colors.ENDC}")
        print("-" * 60)
        
        choice = input(f"{Colors.YELLOW}Select option [1-3, or 99/b]: {Colors.ENDC}").strip().lower()
        if choice in ["99", "b", "back"]:
            break
        elif choice == "1":
            u = input(f"{Colors.YELLOW}Enter Webhook URL: {Colors.ENDC}").strip()
            if u:
                WEBHOOK_CONFIG["url"] = u
                print(f"{Colors.GREEN}[✔] Webhook URL configured successfully.{Colors.ENDC}")
                input(f"{Colors.YELLOW}Press Enter...{Colors.ENDC}")
        elif choice == "2":
            print(f"{Colors.GREEN}[+] Dispatching test notification...{Colors.ENDC}")
            send_notification("Test dispatch from Magic Hat Framework.")
            print(f"{Colors.GREEN}[✔] Test alert sent.{Colors.ENDC}")
            input(f"{Colors.YELLOW}Press Enter...{Colors.ENDC}")
        elif choice == "3":
            WEBHOOK_CONFIG["url"] = ""
            print(f"{Colors.YELLOW}[*] Webhook notifications disabled.{Colors.ENDC}")
            input(f"{Colors.YELLOW}Press Enter...{Colors.ENDC}")


def handle_quick_shell():
    """Phase 9: Operator Quick-Shell Launcher."""
    clear_screen()
    print_tactical_header()
    print("=== OPERATOR QUICK-SHELL ===".center(60))
    print("Type any command to execute in the system shell.")
    print("Type 'exit' or 'back' to return to the framework menu.")
    print("-" * 60)
    
    while True:
        cmd = input(f"{Colors.GREEN}magic-hat-shell# {Colors.ENDC}").strip()
        if not cmd:
            continue
        if cmd.lower() in ["exit", "back", "99"]:
            break
            
        try:
            subprocess.run(cmd, shell=True)
        except Exception as e:
            print(f"{Colors.RED}[-] Execution error: {e}{Colors.ENDC}")
        print()


def handle_wordlist_manager():
    """Tool 16: Integrated Wordlist Manager."""
    clear_screen()
    print_tactical_header()
    print("=== INTEGRATED WORDLIST MANAGER ===".center(60))
    print("-" * 60)
    wordlist_path = "/data/data/com.termux/files/usr/share/wordlists/dirb/common.txt"
    print(f"[*] Default Wordlist Path: {wordlist_path}")
    
    exists = os.path.exists(wordlist_path)
    status_str = f"{Colors.GREEN}FOUND [✔]{Colors.ENDC}" if exists else f"{Colors.RED}MISSING [✘]{Colors.ENDC}"
    print(f"[*] Status: {status_str}")
    
    if not exists:
        print(f"{Colors.GREEN}\n[+] Creating standard fallback wordlist directory & file...{Colors.ENDC}")
        try:
            os.makedirs(os.path.dirname(wordlist_path), exist_ok=True)
            sample_words = ["admin", "login", "dashboard", "api", "config.json", "secret", "backup", "test", "uploads", "wp-admin", "server-status"]
            with open(wordlist_path, "w") as wf:
                wf.write("\n".join(sample_words) + "\n")
            print(f"{Colors.GREEN}[✔] Fallback common wordlist created successfully!{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}[-] Failed to create wordlist: {e}{Colors.ENDC}")
    else:
        print(f"{Colors.GREEN}[✔] Wordlist is verified and ready for FFUF and audit tools.{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")


def handle_view_logs():
    """Phase 10: Display past scan logs stored in the database and view full output."""
    while True:
        clear_screen()
        print_tactical_header()
        print("=== SCAN ARCHIVES (LOGS) ===".center(60))
        print("-" * 60)
        
        logs = get_scan_logs()
        if not logs:
            print(f"{Colors.YELLOW}No scan logs found in the archives yet.{Colors.ENDC}")
            input(f"{Colors.YELLOW}\nPress Enter to return to the main menu...{Colors.ENDC}")
            break
            
        print(f"{'ID':<4} | {'Tool':<16} | {'Target':<15} | {'Timestamp'}")
        print("=" * 60)
        for log in logs:
            print(f"{log['id']:<4} | {log['tool_name']:<16} | {log['target']:<15} | {log['timestamp']}")
            
        print("-" * 60)
        view_id = input(f"{Colors.YELLOW}Enter log ID to view full output (or press Enter to go back): {Colors.ENDC}").strip()
        if not view_id:
            break
            
        if view_id.isdigit():
            with get_connection() as conn:
                row = conn.execute("SELECT tool_name, target, timestamp, output, metadata FROM scan_logs WHERE id = ?", (view_id,)).fetchone()
                if row:
                    clear_screen()
                    print_tactical_header()
                    print(f"=== LOG DETAILS [ID: {view_id}] ===".center(60))
                    print(f"Tool:     {row['tool_name']}")
                    print(f"Target:   {row['target']}")
                    print(f"Time:     {row['timestamp']}")
                    if row['metadata']:
                        print(f"Metadata: {row['metadata']}")
                    print("-" * 60)
                    print(row['output'])
                    print("-" * 60)
                else:
                    print(f"{Colors.RED}\n[-] Error: Log ID not found.{Colors.ENDC}")
            input(f"{Colors.YELLOW}\nPress Enter to continue...{Colors.ENDC}")
        else:
            print(f"{Colors.RED}\n[-] Invalid input. Please enter a numeric ID.{Colors.ENDC}")
            input(f"{Colors.YELLOW}\nPress Enter to continue...{Colors.ENDC}")
