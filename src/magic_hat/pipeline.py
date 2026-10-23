"""Automated multi-stage reconnaissance pipeline for Magic Hat."""

import threading
import subprocess
import time
from magic_hat.database import log_scan
from magic_hat.utils import BANNER_IMAGE, clear_screen, get_all_device_ips, get_subnet_range, print_tactical_header, Colors
import magic_hat.utils as utils

def _background_pipeline_task():
    """Execute multi-stage discovery in a background daemon thread with notifications."""
    utils.PIPELINE_STATE = f"{Colors.YELLOW}RUNNING...{Colors.ENDC}"
    try:
        ips = get_all_device_ips()
        if ips:
            _, ip_cidr = ips[0]
            subnet = get_subnet_range(ip_cidr)
            
            # Stage 1: Subnet Host Sweep
            cmd1 = ["nmap", "-sn", subnet]
            res1 = subprocess.run(cmd1, capture_output=True, text=True, check=True)
            log_scan("Pipeline Stage 1: Sweep", subnet, res1.stdout)

            # Stage 2: Top Port Scan on Subnet
            cmd2 = ["nmap", "-T4", "--top-ports", "100", subnet]
            res2 = subprocess.run(cmd2, capture_output=True, text=True, check=True)
            log_scan("Pipeline Stage 2: Port Scan", subnet, res2.stdout)
            
        utils.PIPELINE_STATE = f"{Colors.GREEN}COMPLETED [✔]{Colors.ENDC}"
        utils.send_notification("Auto-Pilot Reconnaissance Pipeline completed successfully!")
    except Exception as e:
        utils.PIPELINE_STATE = f"{Colors.RED}FAILED [✘]{Colors.ENDC}"
        utils.send_notification(f"Auto-Pilot Reconnaissance Pipeline failed: {e}")

def run_interactive_pipeline_with_progress():
    """Execute multi-stage discovery in foreground with a live Rich progress bar."""
    from magic_hat.utils import create_tactical_progress
    
    ips = get_all_device_ips()
    if not ips:
        print(f"{Colors.RED}[-] No active network interface detected.{Colors.ENDC}")
        return
        
    _, ip_cidr = ips[0]
    subnet = get_subnet_range(ip_cidr)
    print(f"{Colors.GREEN}[*] Target Subnet Space: {subnet}{Colors.ENDC}\n")
    
    progress = create_tactical_progress()
    if progress:
        with progress:
            task = progress.add_task("[bold green]Auto-Pilot Recon Pipeline[/bold green]", total=100)
            
            # Stage 1: Sweep
            progress.update(task, description="[bold green]Stage 1/2: Host Sweep (-sn)...[/bold green]", completed=15)
            cmd1 = ["nmap", "-sn", subnet]
            try:
                res1 = subprocess.run(cmd1, capture_output=True, text=True, check=True)
                log_scan("Pipeline Stage 1: Sweep", subnet, res1.stdout)
            except Exception as e:
                print(f"\n{Colors.RED}[-] Stage 1 failed: {e}{Colors.ENDC}")
                return
            progress.update(task, completed=50)
            
            # Stage 2: Top Ports
            progress.update(task, description="[bold green]Stage 2/2: Top 100 Port Sweep...[/bold green]", completed=65)
            cmd2 = ["nmap", "-T4", "--top-ports", "100", subnet]
            try:
                res2 = subprocess.run(cmd2, capture_output=True, text=True, check=True)
                log_scan("Pipeline Stage 2: Port Scan", subnet, res2.stdout)
            except Exception as e:
                print(f"\n{Colors.RED}[-] Stage 2 failed: {e}{Colors.ENDC}")
                return
            progress.update(task, description="[bold green]Pipeline Telemetry Synchronized [✔][/bold green]", completed=100)
    else:
        _background_pipeline_task()

    print(f"\n{Colors.GREEN}[✔] Multi-stage tactical pipeline completed and saved to database.{Colors.ENDC}")
    utils.send_notification(f"Auto-Pilot Reconnaissance Pipeline completed on {subnet}")


def run_autopilot_pipeline():
    """Trigger background or live foreground pipeline execution."""
    clear_screen()
    print_tactical_header()
    print("=== AUTO-PILOT RECONNAISSANCE PIPELINE ===".center(60))
    print("-" * 60)
    print(f"{Colors.DIM}Description: Multi-stage subnet discovery & port profiling.{Colors.ENDC}")
    print("-" * 60)
    print(f"[*] Current Background State: {utils.PIPELINE_STATE}")
    print("-" * 60)
    print(f"{Colors.BOLD}1.{Colors.ENDC} Run Foreground Pipeline (Live Tactical Progress Bar)")
    print(f"{Colors.BOLD}2.{Colors.ENDC} Launch in Background (Daemon Thread)")
    print(f"{Colors.RED}99. Back to Main Menu (b){Colors.ENDC}")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select mode [1-2, or 99/b]: {Colors.ENDC}").strip().lower()
    if choice in ["99", "b", "back"]:
        return
    elif choice == "1":
        run_interactive_pipeline_with_progress()
    elif choice == "2":
        if "RUNNING..." in utils.PIPELINE_STATE:
            print(f"{Colors.YELLOW}[!] Pipeline is already executing in the background...{Colors.ENDC}")
        else:
            t = threading.Thread(target=_background_pipeline_task, daemon=True)
            t.start()
            print(f"{Colors.GREEN}[✔] Pipeline dispatched to background. Status will update under banner.{Colors.ENDC}")
            
    time.sleep(1)
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")