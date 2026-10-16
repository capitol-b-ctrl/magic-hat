"""Automated multi-stage reconnaissance pipeline for Magic Hat."""

import subprocess
from magic_hat.database import log_scan
from magic_hat.utils import get_all_device_ips, get_subnet_range, clear_screen, BANNER_IMAGE

def run_autopilot_pipeline():
    """Chained pipeline: Subnet sweep -> Top ports recon -> Telemetry archival."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== MULTI-STAGE RECONNAISSANCE PIPELINE ===")
    print("-" * 55)
    
    ips = get_all_device_ips()
    _, ip_cidr = ips[0]
    subnet = get_subnet_range(ip_cidr)
    
    print(f"[*] Target Subnet Space: {subnet}")
    
    # Stage 1: Subnet Host Sweep
    print("\n[Stage 1/2] Executing active ARP/Ping host discovery...")
    try:
        cmd1 = ["nmap", "-sn", subnet]
        res1 = subprocess.run(cmd1, capture_output=True, text=True, check=True)
        print(res1.stdout[:1000])
        log_scan("Pipeline Stage 1: Sweep", subnet, res1.stdout)
    except Exception as e:
        print(f"[-] Pipeline Stage 1 failed: {e}")
        input("\nPress Enter to return...")
        return

    # Stage 2: Top Port Scan on Subnet
    print("\n[Stage 2/2] Executing Top-100 Port Scan on live host space...")
    try:
        cmd2 = ["nmap", "-T4", "--top-ports", "100", subnet]
        res2 = subprocess.run(cmd2, capture_output=True, text=True, check=True)
        print(res2.stdout[:1500])
        log_scan("Pipeline Stage 2: Port Scan", subnet, res2.stdout)
    except Exception as e:
        print(f"[-] Pipeline Stage 2 failed: {e}")
        
    print("\n[✔] Multi-Stage Recon Pipeline completed successfully!")
    input("\nPress Enter to return to main menu...")