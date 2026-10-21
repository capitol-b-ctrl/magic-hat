"""Automated remote telemetry and session management agent for Magic Hat."""

import paramiko
from magic_hat.database import log_scan_result
from magic_hat.utils import Colors, clear_screen, print_tactical_header, load_config

def run_remote_telemetry_agent():
    """Connects to the global target or default router, pulls telemetry, and logs it."""
    clear_screen()
    print_tactical_header()
    print("=== AUTOMATED REMOTE TELEMETRY AGENT ===".center(60))
    print("-" * 60)
    
    # Load config or default to your GL.iNet router
    config = load_config() or {}
    target_ip = config.get("global_target", "192.168.8.1")
    port = int(config.get("ssh_port", 2222))
    username = "root"
    password = "Magician$612"
    
    print(f"[*] Target Scope : {target_ip}:{port}")
    print(f"[*] User         : {username}")
    print("-" * 60)
    
    confirm = input(f"{Colors.YELLOW}Execute automated remote telemetry audit? (Y/N): {Colors.ENDC}").strip().lower()
    if confirm in ['n', 'no']:
        return

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        print(f"\n{Colors.YELLOW}[*] Establishing secure SSH session to {target_ip}...{Colors.ENDC}")
        client.connect(target_ip, port=port, username=username, password=password, timeout=5)
        print(f"{Colors.GREEN}[✔] Authentication successful! Gathering system state...{Colors.ENDC}")
        
        commands = [
            "uptime",
            "iwinfo",
            "cat /proc/loadavg",
            "netstat -an | grep ESTABLISHED",
            "uci show wireless"
        ]
        
        aggregated_output = ""
        for cmd in commands:
            print(f"    -> Running: {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            output = stdout.read().decode()
            error = stderr.read().decode()
            aggregated_output += f"--- CMD: {cmd} ---\n{output}\n"
            if error:
                aggregated_output += f"STDERR:\n{error}\n"
            
        # Log results to Magic Hat SQLite database
        log_scan_result("Remote-Telemetry-Agent", target_ip, aggregated_output)
        print(f"\n{Colors.GREEN}[+] Telemetry successfully pulled and archived into database!{Colors.ENDC}")
        
    except Exception as e:
        print(f"\n{Colors.RED}[-] Remote telemetry collection failed: {e}{Colors.ENDC}")
    finally:
        client.close()
        input(f"\n{Colors.YELLOW}Press Enter to return to main menu...{Colors.ENDC}")
