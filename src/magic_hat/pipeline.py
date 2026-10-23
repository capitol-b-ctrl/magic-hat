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

def run_autopilot_pipeline():
    """Trigger background pipeline execution and return instantly to menu."""
    clear_screen()
    print_tactical_header()
    print("=== AUTO-PILOT RECONNAISSANCE PIPELINE ===".center(60))
    print("-" * 60)
    print(f"{Colors.DIM}Description: Runs multi-stage subnet discovery asynchronously.{Colors.ENDC}")
    print("-" * 60)
    
    if "RUNNING..." in utils.PIPELINE_STATE:
        print(f"{Colors.YELLOW}[!] Pipeline is already executing in the background...{Colors.ENDC}")
    else:
        print(f"[*] Current Pipeline State: {utils.PIPELINE_STATE}")
        choice = input(f"{Colors.YELLOW}Launch pipeline in background? [Y/N]: {Colors.ENDC}").strip().lower()
        if choice in ['y', 'yes']:
            t = threading.Thread(target=_background_pipeline_task, daemon=True)
            t.start()
            print(f"{Colors.GREEN}[✔] Pipeline dispatched to background. Status will update under banner.{Colors.ENDC}")
        else:
            print(f"{Colors.YELLOW}[*] Returning to main menu.{Colors.ENDC}")
            
    time.sleep(1)
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")