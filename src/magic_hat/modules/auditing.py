"""Auditing, exploitation, and credential assessment modules for Magic Hat."""

import re
import shutil
import subprocess
from magic_hat.database import log_scan_result
from magic_hat.utils import (
    BANNER_IMAGE,
    clear_screen,
    print_tactical_header,
    Colors
)
from magic_hat.modules.base import (
    print_target_context,
    select_target_interactive
)


def handle_hydra_audit():
    """Phase 3 / Tool 10: Credential & Service Auditor (hydra wrapper)."""
    print_target_context("=== PAGE: CREDENTIAL AUDITOR (HYDRA) ===")
    
    use_intel = input(f"{Colors.YELLOW}Select target from intelligence database? [Y/N]: {Colors.ENDC}").strip().lower()
    target = None
    if use_intel in ['y', 'yes']:
        target = select_target_interactive()
        
    if not target:
        target = input(f"{Colors.YELLOW}Enter target IP/hostname (or 'b' to back): {Colors.ENDC}").strip()
        if target.lower() in ["b", "99", "back", ""]:
            return
            
    print(f"{Colors.GREEN}[*] Target Locked: {target}{Colors.ENDC}")
    service = input(f"{Colors.YELLOW}Enter service protocol (ssh, ftp, http-post-form): {Colors.ENDC}").strip()
    user = input(f"{Colors.YELLOW}Enter username or user file path: {Colors.ENDC}").strip()
    wordlist = input(f"{Colors.YELLOW}Enter password wordlist path: {Colors.ENDC}").strip()
    
    if not all([target, service, user, wordlist]):
        input(f"{Colors.RED}\n[-] All fields are required. Press Enter to return...{Colors.ENDC}")
        return
        
    print(f"{Colors.GREEN}\n[+] Launching Hydra brute-force audit against {target} ({service})...{Colors.ENDC}")
    try:
        cmd = ["hydra", "-l", user, "-P", wordlist, target, service]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print_tactical_header()
        print(f"=== HYDRA AUDIT RESULTS ===".center(60))
        print(output)
        
        log_scan_result("Hydra Audit", f"{service}://{target}", output)
        print(f"{Colors.GREEN}\n[✔] Credential audit logged to database.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}\n[-] Hydra execution failed: {e}{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")


def handle_ssh_audit():
    """Tool 7: SSH Remote Execution & Banner/Key Auditor."""
    print_target_context("=== PAGE: SSH AUDITOR & REMOTE ACCESS ===")
    
    use_intel = input(f"{Colors.YELLOW}Select target from intelligence database? [Y/N]: {Colors.ENDC}").strip().lower()
    target = None
    if use_intel in ['y', 'yes']:
        target = select_target_interactive()
        
    if not target:
        target = input(f"{Colors.YELLOW}Enter target IP/hostname (or 'b' to back): {Colors.ENDC}").strip()
        if target.lower() in ["b", "99", "back", ""]:
            return
            
    port = input(f"{Colors.YELLOW}Enter SSH Port [default 22]: {Colors.ENDC}").strip() or "22"
    user = input(f"{Colors.YELLOW}Enter SSH Username [default root]: {Colors.ENDC}").strip() or "root"
    
    print("\nSelect Action:")
    print(f"{Colors.BOLD}1.{Colors.ENDC} Audit Banner & Key Exchange Algorithms (ssh-keyscan)")
    print(f"{Colors.BOLD}2.{Colors.ENDC} Test Remote SSH Interactive Connection")
    print(f"{Colors.BOLD}3.{Colors.ENDC} Execute Single Remote Command")
    
    choice = input(f"{Colors.YELLOW}Select action [1-3]: {Colors.ENDC}").strip()
    
    if choice == "1":
        print(f"{Colors.GREEN}\n[+] Querying SSH key signatures for {target}:{port}...{Colors.ENDC}")
        try:
            cmd = ["ssh-keyscan", "-p", port, target]
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            output = res.stdout if res.stdout else res.stderr
            
            clear_screen()
            print_tactical_header()
            print(f"=== SSH KEYSCAN TELEMETRY: {target} ===".center(60))
            print(output)
            
            log_scan_result("SSH Keyscan", f"{target}:{port}", output)
            print(f"{Colors.GREEN}\n[✔] SSH key telemetry logged to database.{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.RED}\n[-] SSH keyscan failed: {e}{Colors.ENDC}")
            
    elif choice == "2":
        print(f"{Colors.GREEN}\n[+] Spawning interactive SSH session to {user}@{target}:{port}...{Colors.ENDC}")
        try:
            subprocess.run(["ssh", "-p", port, f"{user}@{target}"])
        except Exception as e:
            print(f"{Colors.RED}\n[-] Interactive SSH failed: {e}{Colors.ENDC}")
            
    elif choice == "3":
        remote_cmd = input(f"{Colors.YELLOW}Enter remote command to execute: {Colors.ENDC}").strip()
        if remote_cmd:
            print(f"{Colors.GREEN}\n[+] Executing '{remote_cmd}' on {target}...{Colors.ENDC}")
            try:
                cmd = ["ssh", "-p", port, f"{user}@{target}", remote_cmd]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
                output = res.stdout
                print(output)
                log_scan_result("SSH Remote Exec", f"{user}@{target}", output)
            except Exception as e:
                print(f"{Colors.RED}\n[-] Remote command failed: {e}{Colors.ENDC}")
                
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")


def handle_powershell_audit():
    """Tool: PowerShell Core (pwsh) & WinRM Remote Management."""
    clear_screen()
    print_tactical_header()
    print("=== PAGE: POWERSHELL CORE & WINRM ===".center(60))
    print("-" * 60)
    
    if not shutil.which("pwsh"):
        print(f"{Colors.RED}\n[-] Notice: 'pwsh' (PowerShell Core) binary is not installed in this environment.{Colors.ENDC}")
        print(f"{Colors.YELLOW}[*] To install in Termux: `pkg install powershell` (if available for your arch).{Colors.ENDC}")
        input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")
        return

    print("Select Mode:")
    print(f"{Colors.BOLD}1.{Colors.ENDC} Run Local PowerShell Command / One-Liner (pwsh -c)")
    print(f"{Colors.BOLD}2.{Colors.ENDC} WinRM Remote Query (WS-Man / Windows Hosts)")
    print(f"{Colors.RED}99. Back (b){Colors.ENDC}")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select option [1-2, or 99/b]: {Colors.ENDC}").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    if choice == "1":
        ps_cmd = input(f"{Colors.YELLOW}Enter PowerShell command: {Colors.ENDC}").strip()
        if not ps_cmd:
            return
        try:
            cmd = ["pwsh", "-NoProfile", "-NonInteractive", "-Command", ps_cmd]
            res = subprocess.run(cmd, capture_output=True, text=True, check=True)
            clear_screen()
            print_tactical_header()
            print("=== POWERSHELL EXECUTION OUTPUT ===".center(60))
            print(res.stdout)
            log_scan_result("PowerShell Command", "Local Host", res.stdout)
        except Exception as e:
            print(f"{Colors.RED}\n[-] PowerShell execution failed: {e}{Colors.ENDC}")
            
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")


def handle_hash_identifier():
    """Tool 8: Hash Identification & Cracking Assistant."""
    clear_screen()
    print_tactical_header()
    print("=== PAGE: HASH IDENTIFIER & AUDIT ===".center(60))
    print("-" * 60)
    
    hash_str = input(f"{Colors.YELLOW}Enter hash string to analyze (or 'b' to back): {Colors.ENDC}").strip()
    if hash_str.lower() in ["b", "99", "back", ""]:
        return
        
    print(f"{Colors.GREEN}[*] Target Hash Locked: {hash_str}{Colors.ENDC}")
    length = len(hash_str)
    identified = []
    
    if length == 32 and re.match(r"^[a-fA-F0-9]{32}$", hash_str):
        identified.append("MD5 / NTLM / MD4")
    elif length == 40 and re.match(r"^[a-fA-F0-9]{40}$", hash_str):
        identified.append("SHA-1 / MySQL")
    elif length == 64 and re.match(r"^[a-fA-F0-9]{64}$", hash_str):
        identified.append("SHA-256 / WPA-PSK TKIP")
    elif hash_str.startswith("$2a$") or hash_str.startswith("$2b$") or hash_str.startswith("$2y$"):
        identified.append("Bcrypt (Blowfish)")
    elif hash_str.startswith("$6$"):
        identified.append("SHA-512 Crypt (Linux)")
    else:
        identified.append("Unknown or complex hash format")
        
    clear_screen()
    print_tactical_header()
    print("=== HASH ANALYSIS RESULTS ===".center(60))
    print(f"[*] Input Hash: {hash_str}")
    print(f"[*] Length: {length} characters")
    print("[*] Potential Formats:")
    for fmt in identified:
        print(f"    - {fmt}")
    print("-" * 60)
    
    run_crack = input(f"{Colors.YELLOW}Would you like to invoke hashcat against this hash? (Y/N): {Colors.ENDC}").strip().lower()
    if run_crack == 'y':
        mode = input(f"{Colors.YELLOW}Enter hashcat mode number (e.g., 0 for MD5, 1000 for NTLM): {Colors.ENDC}").strip()
        wordlist = input(f"{Colors.YELLOW}Enter wordlist path: {Colors.ENDC}").strip()
        if mode and wordlist:
            print(f"{Colors.GREEN}\n[+] Launching hashcat audit...{Colors.ENDC}")
            try:
                cmd = ["hashcat", "-a", "0", "-m", mode, hash_str, wordlist]
                res = subprocess.run(cmd, capture_output=True, text=True, check=True)
                print(res.stdout)
                log_scan_result("Hash Audit", hash_str, res.stdout)
            except Exception as e:
                print(f"{Colors.RED}\n[-] Hashcat execution failed: {e}{Colors.ENDC}")
                
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")


def handle_exploit_search():
    """Tool 9: Exploit Search Engine (searchsploit wrapper)."""
    print_target_context("=== PAGE: EXPLOIT SEARCH ENGINE ===")
    
    query = input(f"{Colors.YELLOW}Enter service or software version (e.g., 'apache 2.4') or 'b' to back: {Colors.ENDC}").strip()
    if query.lower() in ["b", "99", "back", ""]:
        return
        
    print(f"{Colors.GREEN}[*] Query Locked: {query}{Colors.ENDC}")
    print(f"{Colors.GREEN}\n[+] Querying local exploit database for '{query}'...{Colors.ENDC}")
    try:
        cmd = ["searchsploit", query]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        
        clear_screen()
        print_tactical_header()
        print(f"=== EXPLOIT RESULTS: {query} ===".center(60))
        print(output)
        
        log_scan_result("Exploit Search", query, output)
        print(f"{Colors.GREEN}\n[✔] Exploit search results logged to database.{Colors.ENDC}")
    except FileNotFoundError:
        print(f"{Colors.RED}\n[-] Error: 'searchsploit' binary not found. Install exploitdb.{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.RED}\n[-] Searchsploit failed: {e}{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")
