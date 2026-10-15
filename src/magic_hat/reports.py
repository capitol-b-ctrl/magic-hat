"""Automated Markdown intelligence report generator for Magic Hat."""

import os
from datetime import datetime
from magic_hat.database import get_scan_logs, get_connection
from magic_hat.utils import BANNER_IMAGE, clear_screen

# Anchor reports locally inside the package directory
PACKAGE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(PACKAGE_DIR, "reports")

def export_scan_report(log_id=None):
    """Export a specific scan log or all logs into a formatted Markdown report."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    timestamp_slug = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    with get_connection() as conn:
        if log_id:
            cursor = conn.execute("SELECT * FROM scan_logs WHERE id = ?", (log_id,))
            row = cursor.fetchone()
            if not row:
                return False, "Log ID not found."
            logs = [dict(row)]
            filename = f"report_log_{log_id}_{timestamp_slug}.md"
        else:
            cursor = conn.execute("SELECT * FROM scan_logs ORDER BY id DESC")
            logs = [dict(row) for row in cursor.fetchall()]
            filename = f"full_engagement_report_{timestamp_slug}.md"
            
    if not logs:
        return False, "No logs available to export."
        
    filepath = os.path.join(REPORTS_DIR, filename)
    
    lines = []
    lines.append("# Magic Hat Intelligence Report")
    lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"**Total Records Exported:** {len(logs)}")
    lines.append("\n---\n")

    for log in logs:
        lines.append(f"## Tool: {log['tool_name']}")
        lines.append(f"* **Target / Interface:** `{log['target']}`")
        lines.append(f"* **Timestamp:** `{log['timestamp']}`")
        lines.append(f"* **Log ID:** `{log['id']}`\n")
        lines.append("```text")
        lines.append(str(log['output']))
        lines.append("```")
        lines.append("\n---\n")

    report_content = "\n".join(lines)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    return True, filepath

def handle_report_menu():
    """Interactive report generation menu."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: AUTOMATED REPORT GENERATOR ===")
    print("-" * 45)
    print("1. Export ALL Engagement Logs to Markdown")
    print("2. Export a Specific Log ID")
    print("3. Return")
    print("-" * 45)
    
    choice = input("Select option [1-3]: ").strip()
    if choice == "1":
        success, path = export_scan_report()
        if success:
            print(f"\n[+] Full report successfully compiled and saved to:\n    {path}")
        else:
            print(f"\n[-] Error: {path}")
        input("\nPress Enter to return...")
    elif choice == "2":
        log_id = input("Enter Log ID to export: ").strip()
        if log_id.isdigit():
            success, path = export_scan_report(log_id)
            if success:
                print(f"\n[+] Report successfully compiled and saved to:\n    {path}")
            else:
                print(f"\n[-] Error: {path}")
        else:
            print("\n[-] Invalid ID.")
        input("\nPress Enter to return...")
