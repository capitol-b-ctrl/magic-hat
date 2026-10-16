
"""Automated Markdown and JSON report generator for Magic Hat security engagements."""

import os
import json
from magic_hat.database import get_connection, get_scan_logs
from magic_hat.utils import clear_screen, BANNER_IMAGE

def export_engagement_report():
    """Export all SQLite scan logs into a structured Markdown and JSON report."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== AUTOMATED ENGAGEMENT REPORT GENERATOR ===")
    print("-" * 55)
    
    logs = get_scan_logs()
    if not logs:
        print("[-] No scan logs found to export.")
        input("\nPress Enter to return...")
        return
        
    report_filename = os.path.expanduser("~/magic_hat_engagement_report.md")
    json_filename = os.path.expanduser("~/magic_hat_telemetry_export.json")
    
    full_data = []
    with get_connection() as conn:
        rows = conn.execute("SELECT id, tool_name, target, metadata_json, output, timestamp FROM scan_logs ORDER BY id DESC").fetchall()
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
            mf.write(f"* **Metadata:** `{item['metadata_json']}`\n\n")
            mf.write("```text\n" + str(item['output'])[:2000] + "\n```\n\n")
            mf.write("---\n\n")
            
    print(f"[✔] Markdown Report successfully exported to: {report_filename}")
    print(f"[✔] JSON Telemetry successfully exported to: {json_filename}")
    input("\nPress Enter to return...")

def handle_report_menu():
    """Report management interface."""
    while True:
        clear_screen()
        print(BANNER_IMAGE)
        print("=== REPORT GENERATION & EXPORT MENU ===")
        print("-" * 55)
        print("1. Export Full Engagement Report (Markdown & JSON)")
        print("99. Back to Main Menu (b)")
        print("-" * 55)
        choice = input("Select option [1, or 99/b]: ").strip().lower()
        if choice in ["99", "b", "back"]:
            break
        elif choice == "1":
            export_engagement_report()
        else:
            input("Invalid selection! Press Enter...")