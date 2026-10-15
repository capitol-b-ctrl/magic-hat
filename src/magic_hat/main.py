"""Main entry point and interactive menu layout for Magic Hat."""

import sys
from magic_hat.utils import BANNER_IMAGE, clear_screen, get_all_device_ips
from magic_hat.database import save_item, get_all_items, search_items, calculate_budget
from magic_hat.tools import handle_pentest_suite_menu, handle_view_logs
from magic_hat.pipeline import run_autopilot_pipeline
from magic_hat.server import run_web_server

def handle_add():
    """Page 1: Add a new prop or item."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: ADD NEW PROP ===")
    
    name = input("Enter item name: ")
    try:
        price = float(input("Enter estimated/actual price ($): "))
    except ValueError:
        price = 0.0
    supplier = input("Enter supplier (leave blank for 'Unknown'): ") or "Unknown"
    
    save_item(name, price, supplier)
    
    print("\n[✔] Conjuring item into the Hat...")
    print(f"[*] Name:     {name}")
    print(f"[*] Price:    ${price:.2f}")
    print(f"[*] Supplier: {supplier}")
    
    input("\nPress Enter to return to the main menu...")

def handle_list():
    """Page 2: List all items."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: INVENTORY LIST ===")
    print("[*] Inspecting the contents of the Hat...")
    print("-" * 45)
    print(f"{'Price':<10} | {'Supplier':<15} | {'Item'}")
    print("-" * 45)
    
    items = get_all_items()
    if not items:
        print("No items found in the Hat yet. Try adding one!")
    else:
        for item in items:
            print(f"${item.get('price', 0):.2f} | {item.get('supplier', 'Unknown'):<15} | {item.get('name', '')}")
            
    input("\nPress Enter to return to the main menu...")

def handle_search():
    """Page 3: Search for an item."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: SEARCH ARCHIVES ===")
    print("-" * 45)
    
    query = input("Enter search keyword: ").strip()
    print(f"\n[🔬] Searching the magical archives for '{query}'...")
    results = search_items(query)
    
    if not results:
        print("No matching items found.")
    else:
        print(f"\nFound {len(results)} matching item(s):")
        print(f"{'Price':<10} | {'Supplier':<15} | {'Item'}")
        print("-" * 45)
        for item in results:
            print(f"${item.get('price', 0):.2f} | {item.get('supplier', 'Unknown'):<15} | {item.get('name', '')}")
            
    input("\nPress Enter to return to the main menu...")

def handle_budget():
    """Page 4: Budget summary."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: BUDGET OVERVIEW ===")
    print("[🧮] Calculating total spell components budget...")
    total = calculate_budget()
    print(f"[*] Total Acquisition Cost: ${total:.2f}")
    
    input("\nPress Enter to return to the main menu...")

"""Main entry point and interactive menu layout for Magic Hat."""


def main():
    """Main tactical application loop."""
    while True:
        clear_screen()
        print(BANNER_IMAGE)
        
        ips = get_all_device_ips()
        ip_str = " | ".join([f"{iface}: {ip}" for iface, ip in ips])
        print(f"[*] Interfaces -> {ip_str}")
        
        # Display live server status
        srv_status = "[ONLINE]" if is_server_running() else "[OFFLINE]"
        
        print("---------------------------------------------")
        print("TACTICAL OPERATIONS MENU")
        print("---------------------------------------------")
        print("1. Offensive Security Suite (Tools)")
        print("2. Auto-Pilot Recon Pipeline")
        print(f"3. Toggle Local Web Dashboard {srv_status}")
        print("4. View Scan Archives (Logs)")
        print("5. Exit")
        print("---------------------------------------------")
        
        choice = input("Select an option [1-5]: ").strip()
        
        if choice == "1":
            handle_pentest_suite_menu()
        elif choice == "2":
            run_autopilot_pipeline()
        elif choice == "3":
            toggle_web_server()
        elif choice == "4":
            handle_view_logs()
        elif choice == "5":
            if is_server_running():
                toggle_web_server()
            clear_screen()
            print("Exiting Magic Hat. Farewell, magician!\n")
            sys.exit(0)
        else:
            input("Invalid selection! Press Enter to try again...")

if __name__ == "__main__":
    main()
