"""Automated Remote Telemetry Agent for Magic Hat framework."""

import paramiko
import sys
from magic_hat.utils import clear_screen, print_tactical_header, Colors
from magic_hat.database import log_scan

def run_remote_telemetry_agent():
    """Connects to the GL.iNet router via Paramiko SSH, executes telemetry diagnostics, and logs output."""
    clear_screen()
    print_tactical_header()
    print("=== AUTOMATED REMOTE TELEMETRY AGENT ===".center(60))
    print("-" * 60)
    
    target = input(f"{Colors.YELLOW}Enter target router IP [default 192.168.8.1]: {Colors.ENDC}").strip() or "192.168.8.1"
    port = int(input(f"{Colors.YELLOW}Enter SSH port [default 2222]: {Colors.ENDC}").strip() or "2222")
    user = input(f"{Colors.YELLOW}Enter SSH username [default root]: {Colors.ENDC}").strip() or "root"
    password = input(f"{Colors.YELLOW}Enter SSH password: {Colors.ENDC}").strip()
    
    print(f"\n{Colors.GREEN}[*] Establishing secure SSH session to {target}:{port}...{Colors.ENDC}")
    
    try:
        # Safely convert the tuple of preferred public keys to a list, append ssh-rsa, and convert back
        try:
            pubkeys = list(paramiko.transport.Transport._preferred_pubkeys)
            if 'ssh-rsa' not in pubkeys:
                pubkeys.append('ssh-rsa')
            paramiko.transport.Transport._preferred_pubkeys = tuple(pubkeys)
        except Exception:
            pass
            
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        client.connect(
            hostname=target,
            port=port,
            username=user,
            password=password,
            timeout=10,
            allow_agent=False,
            look_for_keys=False
        )
        
        print(f"{Colors.GREEN}[✔] Authenticated successfully. Gathering remote telemetry...{Colors.ENDC}")
        
        # Execute diagnostic commands on the router
        commands = [
            "uname -a",
            "uptime",
            "cat /etc/openwrt_release",
            "df -h",
            "ubus call system board"
        ]
        
        telemetry_output = ""
        for cmd in commands:
            stdin, stdout, stderr = client.exec_command(cmd)
            out = stdout.read().decode('utf-8')
            err = stderr.read().decode('utf-8')
            telemetry_output += f"--- CMD: {cmd} ---\n{out}\n{err}\n"
            
        client.close()
        
        clear_screen()
        print_tactical_header()
        print(f"=== REMOTE TELEMETRY REPORT: {target} ===".center(60))
        print(telemetry_output)
        print("-" * 60)
        
        log_scan("Remote Telemetry Agent", target, telemetry_output)
        print(f"{Colors.GREEN}[✔] Remote telemetry logged to database successfully.{Colors.ENDC}")
        
    except Exception as e:
        print(f"{Colors.RED}\n[-] Remote telemetry collection failed: {e}{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return to main menu...{Colors.ENDC}")
