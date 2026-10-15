"""Automated multi-tool recon pipeline for Magic Hat."""

import subprocess
from magic_hat.database import log_scan
from magic_hat.reports import export_scan_report
from magic_hat.utils import BANNER_IMAGE, clear_screen, send_webhook_notification

def run_autopilot_pipeline():
    """Execute an automated chain: Nmap version scan -> Tech fingerprinting -> Report generation."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: AUTO-PILOT RECON PIPELINE ===")
    print("-" * 45)
    
    target = input("Enter target IP, domain, or CIDR for automated audit: ").strip()
    if not target:
        return
        
    print(f"\n[+] [Step 1/3] Running Nmap Version & Service Scan on {target}...")
    print("[*] Please wait, version scans take a moment. Press Ctrl+C to abort safely.\n")
    
    try:
        cmd = ["nmap", "-sV", "-T4", target]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        output = result.stdout
        print(output)
        log_scan("AutoPilot Nmap", target, output)
        print("[✔] Nmap scan completed and logged to database.")
    except KeyboardInterrupt:
        print("\n\n[-] Pipeline interrupted by user. Returning to main menu...")
        input("\nPress Enter to return...")
        return
    except Exception as e:
        print(f"\n[-] Nmap step failed: {e}")
        input("\nPress Enter to return...")
        return
        
    print(f"\n[+] [Step 2/3] Running Web Tech Fingerprint (WhatWeb) on {target}...")
    try:
        web_cmd = ["whatweb", f"http://{target}"]
        web_res = subprocess.run(web_cmd, capture_output=True, text=True, check=True)
        print(web_res.stdout)
        log_scan("AutoPilot Fingerprint", target, web_res.stdout)
        print("[✔] Tech fingerprint completed and logged.")
    except KeyboardInterrupt:
        print("\n\n[-] Pipeline interrupted by user.")
        input("\nPress Enter to return...")
        return
    except Exception:
        print("[*] Web fingerprint skipped or target does not host standard web ports.")
        
    print(f"\n[+] [Step 3/3] Compiling consolidated engagement markdown report...")
    success, path = export_scan_report()
    if success:
        print(f"[✔] Pipeline complete! Report compiled at:\n    {path}")
        send_webhook_notification("Auto-Pilot Pipeline Complete", f"Finished automated audit on {target}")
    
    input("\nPress Enter to return...")
