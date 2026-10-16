"""Automated multi-stage reconnaissance pipeline for Magic Hat."""

import threading
import subprocess
from magic_hat.database import log_scan
from magic_hat.utils import get_all_device_ips, get_subnet_range, print_tactical_header
import magic_hat.utils as utils

def _background_pipeline_task():
    """Execute multi-stage discovery in a background daemon thread."""
    utils.PIPELINE_STATE = "RUNNING..."
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
            
        utils.PIPELINE_STATE = "COMPLETED [✔]"
    except Exception as e:
        utils.PIPELINE_STATE = f"FAILED [✘]"

def run_autopilot_pipeline():
    """Trigger background pipeline execution and return instantly to menu."""
    print_tactical_header()
    print("=== AUTO-PILOT RECONNAISSANCE PIPELINE ===")
    print("Description: Runs multi-stage subnet discovery asynchronously.")
    print("-" * 55)
    
    if utils.PIPELINE_STATE == "RUNNING...":
        print("[!] Pipeline is already executing in the background...")
    else:
        print(f"Current Pipeline State: {utils.PIPELINE_STATE}")
        choice = input("Launch pipeline in background? [y/N]: ").strip().lower()
        if choice in ['y', 'yes']:
            t = threading.Thread(target=_background_pipeline_task, daemon=True)
            t.start()
            print("[✔] Pipeline dispatched to background. Status will update under banner.")
        else:
            print("[*] Returning to main menu.")
            
    import time
    time.sleep(1)
    
    
    input("\nPress Enter to return to main menu...")
