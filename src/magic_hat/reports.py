"""Automated Markdown and JSON report generator for Magic Hat security engagements."""

import os
import json
from magic_hat.database import (
    get_scan_logs, 
    get_connection,
    clear_scan_logs
)
from magic_hat.utils import (
    clear_screen, 
    BANNER_IMAGE, 
    print_tactical_header, 
    Colors
)

def export_engagement_report():
    """Export all SQLite scan logs into a structured Markdown and JSON report."""
    clear_screen()
    print_tactical_header()
    print("=== ENGAGEMENT REPORT GENERATOR ===".center(60))
    print("-" * 60)
    
    logs = get_scan_logs()
    if not logs:
        print(f"{Colors.RED}[-] No scan logs found to export.{Colors.ENDC}")
        input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")
        return
        
    report_filename = os.path.expanduser("~/Magic_Hat/src/magic_hat/reports/magic_hat_engagement_report.md")
    json_filename = os.path.expanduser("~/Magic_Hat/src/magic_hat/reports/magic_hat_telemetry_export.json")
    os.makedirs(os.path.dirname(report_filename), exist_ok=True)
    
    full_data = []
    with get_connection() as conn:
        rows = conn.execute("SELECT id, tool_name, target, metadata, output, timestamp FROM scan_logs ORDER BY id DESC").fetchall()
        for r in rows:
            full_data.append(dict(r))
            
    # Write JSON export
    with open(json_filename, "w") as jf:
        json.dump(full_data, jf, indent=4)
        
    # Write Markdown report
    with open(report_filename, "w") as mf:
        mf.write("# Magic Hat Security Engagement Report\n\n")
        mf.write(f"**Total Records Captured:** {len(full_data)}\n\n")
        mf.write("---\n\n## Executive Summary\n")
        mf.write("This report aggregates telemetry, host discoveries, and service scans executed during the tactical engagement.\n\n")
        mf.write("---\n\n## Detailed Scan Telemetry Logs\n\n")
        
        for item in full_data:
            mf.write(f"### Log ID: {item['id']} - {item['tool_name']}\n")
            mf.write(f"* **Target Space:** `{item['target']}`\n")
            mf.write(f"* **Timestamp:** `{item['timestamp']}`\n")
            mf.write(f"* **Metadata:** `{item.get('metadata')}`\n\n")
            mf.write("```text\n" + str(item['output'])[:2000] + "\n```\n\n")
            mf.write("---\n\n")
            
    print(f"{Colors.GREEN}[✔] Markdown Report successfully exported to: {report_filename}{Colors.ENDC}")
    print(f"{Colors.GREEN}[✔] JSON Telemetry successfully exported to: {json_filename}{Colors.ENDC}")
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def confirm_and_clear_database():
    """Prompt user for confirmation before purging all telemetry records."""
    clear_screen()
    print_tactical_header()
    print("=== PURGE TELEMETRY DATABASE ===".center(60))
    print("-" * 60)
    print(f"{Colors.RED}[!] WARNING: This will permanently delete all scan logs and archives!{Colors.ENDC}")
    
    confirm = input(f"{Colors.YELLOW}Are you sure you want to clear the database? Type 'YES' to confirm: {Colors.ENDC}").strip()
    if confirm == "YES":
        clear_scan_logs()
        print(f"{Colors.GREEN}\n[✔] Telemetry database successfully purged. All logs cleared.{Colors.ENDC}")
    else:
        print(f"{Colors.YELLOW}\n[-] Purge aborted. Database remains unchanged.{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")

def handle_report_menu():
    """Report management interface."""
    while True:
        clear_screen()
        print_tactical_header()
        print("=== REPORT GENERATION & EXPORT MENU ===".center(60))
        print("-" * 60)
        print(f"{Colors.BOLD}1.{Colors.ENDC} Export Full Engagement Report (Markdown & JSON)")
        print(f"{Colors.BOLD}2.{Colors.ENDC} Purge & Clear All Scan Logs / Telemetry Database")
        print(f"{Colors.RED}99. Back to Main Menu (b){Colors.ENDC}".center(68, " "))
        print("-" * 60)
        
        choice = input(f"{Colors.YELLOW}Select option [1-2, or 99/b]: {Colors.ENDC}").strip().lower()
        if choice in ["99", "b", "back"]:
            break
        elif choice == "1":
            export_engagement_report()
        elif choice == "2":
            confirm_and_clear_database()
        else:
            input(f"{Colors.RED}Invalid selection! Press Enter...{Colors.ENDC}")
