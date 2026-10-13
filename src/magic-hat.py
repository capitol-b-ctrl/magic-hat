#!/usr/bin/env python3

"""
==============================================================
   MAGIC HAT - A tool by the magician to assist in merchandise acquisition.
   Written in Python
==============================================================
"""

import argparse
import sys

#   GLOBAL CONSTANTS / CONFIGURATION

BANNER_IMAGE = r"""
 .--..--..--..--..--..--..--..--..--..--..--..--..--..--..--.
/ .. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \
\ \/\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ \/ /
 \/ /`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'\/ /
 / /\   /$$      /$$                     /$$             / /\
/ /\ \ | $$$    /$$$                    |__/            / /\ \
\ \/ / | $$$$  /$$$$  /$$$$$$   /$$$$$$  /$$  /$$$$$$$  \ \/ /
 \/ /  | $$ $$/$$ $$ |____  $$ /$$__  $$| $$ /$$_____/   \/ /
 / /\  | $$  $$$| $$  /$$$$$$$| $$  \ $$| $$| $$         / /\
/ /\ \ | $$\  $ | $$ /$$__  $$| $$  | $$| $$| $$        / /\ \
\ \/ / | $$ \/  | $$|  $$$$$$$|  $$$$$$$| $$|  $$$$$$$  \ \/ /
 \/ /  |__/     |__/ \_______/ \____  $$|__/ \_______/   \/ /
 / /\                          /$$  \ $$                 / /\
/ /\ \                        |  $$$$$$/                / /\ \
\ \/ /                         \______/                 \ \/ /
 \/ /   /$$   /$$             /$$                        \/ /
 / /\  | $$  | $$            | $$                        / /\
/ /\ \ | $$  | $$  /$$$$$$  /$$$$$$                     / /\ \
\ \/ / | $$$$$$$$ |____  $$|_  $$_/                     \ \/ /
 \/ /  | $$__  $$  /$$$$$$$  | $$                        \/ /
 / /\  | $$  | $$ /$$__  $$  | $$ /$$                    / /\
/ /\ \ | $$  | $$|  $$$$$$$  |  $$$$/                   / /\ \
\ \/ / |__/  |__/ \_______/   \___/                     \ \/ /
 \/ /                                                    \/ /
 / /\.--..--..--..--..--..--..--..--..--..--..--..--..--./ /\
/ /\ \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \.. \/\ \
\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `'\ `' /
 `--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'`--'

"""


#   CORE FUNCTIONS FOR ACQUISITION FEATURES


print(BANNER_IMAGE)



def clear_screen():
    """Clears the terminal screen and resets the cursor to the top."""
    print("\033[2J\033[H", end="")

# INTERACTIVE PAGE FUNCTIONS

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
    
    print("\n[✔] Conjuring item into the Hat...")
    print(f"[*] Name:      {name}")
    print(f"[*] Price:     ${price:.2f}")
    print(f"[*] Supplier:  {supplier}")
    # TODO: Save to a JSON or SQLite database file
    
    input("\nPress Enter to return to the main menu...")

def handle_list():
    """Page 2: List all items."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: INVENTORY LIST ===")
    print("[📋] Inspecting the contents of the Hat...")
    print("-" * 45)
    print("Price | Supplier | Item")
    print("-" * 45)
    print("No items found in the Hat yet. Try adding one!")
    
    input("\nPress Enter to return to the main menu...")

def handle_search():
    """Page 3: Search for an item."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: SEARCH ARCHIVES ===")
    
    query = input("Enter search keyword: ")
    print(f"\n[🔍] Searching the magical archives for '{query}'...")
    # TODO: Filter items matching query
    
    input("\nPress Enter to return to the main menu...")

def handle_budget():
    """Page 4: Budget summary."""
    clear_screen()
    print(BANNER_IMAGE)
    print("=== PAGE: BUDGET OVERVIEW ===")
    print("[💰] Calculating total spell components budget...")
    print("[*] Total Acquisition Cost: $0.00")
    # TODO: Sum up prices of items
    
    input("\nPress Enter to return to the main menu...")

# MAIN APPLICATION LOOP

def main():
    while True:
        clear_screen()
        print(BANNER_IMAGE)
        print("MAIN MENU")
        print("---------------------------------------------")
        print("1. Add a new prop or item")
        print("2. List all items in the Hat")
        print("3. Search for an item")
        print("4. Show total acquisition budget")
        print("5. Exit")
        print("---------------------------------------------")
        
        choice = input("Select a page number [1-5]: ").strip()
        
        if choice == "1":
            handle_add()
        elif choice == "2":
            handle_list()
        elif choice == "3":
            handle_search()
        elif choice == "4":
            handle_budget()
        elif choice == "5":
            clear_screen()
            print("Exiting Magic Hat. Farewell, magician!")
            sys.exit(0)
        else:
            input("Invalid selection! Press Enter to try again...")

if __name__ == "__main__":
    main()
