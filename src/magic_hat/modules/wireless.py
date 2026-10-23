"""Wireless, RF footprinting, and Bluetooth assessment modules for Magic Hat."""

import shutil
import subprocess
from magic_hat.database import log_scan_result
from magic_hat.utils import (
    BANNER_IMAGE,
    clear_screen,
    print_tactical_header,
    Colors
)
from magic_hat.modules.base import require_root


def handle_wireless_recon():
    """Tool 6: Wireless & RF Footprinting with fallback interface checks."""
    clear_screen()
    print_tactical_header()
    print("=== PAGE: WIRELESS & RF FOOTPRINTING ===".center(60))
    print("-" * 60)
    print(f"{Colors.BOLD}1.{Colors.ENDC} List Wireless Interfaces & Status (iw / nmcli / ip link)")
    print(f"{Colors.BOLD}2.{Colors.ENDC} Scan Nearby Wi-Fi Networks")
    print(f"{Colors.RED}99. Back to Suite Menu (b){Colors.ENDC}")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select option [1-2, or 99/b]: {Colors.ENDC}").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    output = ""
    if choice == "1":
        print(f"{Colors.GREEN}\n[+] Querying wireless subsystem...{Colors.ENDC}")
        try:
            if shutil.which("iw"):
                res = subprocess.run(["iw", "dev"], capture_output=True, text=True, check=True)
                output = res.stdout
            elif shutil.which("nmcli"):
                res = subprocess.run(["nmcli", "device", "wifi"], capture_output=True, text=True, check=True)
                output = res.stdout
            elif shutil.which("ip"):
                res = subprocess.run(["ip", "link"], capture_output=True, text=True, check=True)
                output = "[*] 'iw' and 'nmcli' not found in sandbox. Fallback to system network links:\n" + res.stdout
            else:
                output = "[-] No wireless control binaries (iw, nmcli) or ip tools found in environment."
        except Exception as e:
            output = f"[-] Wireless query failed: {e}"
            
    elif choice == "2":
        print(f"{Colors.GREEN}\n[+] Scanning nearby Wi-Fi networks...{Colors.ENDC}")
        try:
            if shutil.which("nmcli"):
                res = subprocess.run(["nmcli", "device", "wifi", "list"], capture_output=True, text=True, check=True)
                output = res.stdout
            else:
                output = "[-] Wi-Fi scanner ('nmcli') requires NetworkManager daemon, which is restricted in Termux without root/proot."
        except Exception as e:
            output = f"[-] Wi-Fi scan failed: {e}"
            
    clear_screen()
    print_tactical_header()
    print("=== WIRELESS / RF TELEMETRY ===".center(60))
    print(output)
    log_scan_result("Wireless Recon", "Airspace", output)
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")


def handle_wireless_bt_scanner():
    """Phase 4: Scan nearby Wi-Fi networks and Bluetooth devices using Termux API or binaries."""
    clear_screen()
    print_tactical_header()
    print("=== OPTION 1: WIRELESS & BLUETOOTH SCAN ===".center(60))
    print("-" * 60)
    
    print(f"{Colors.GREEN}[*] Scanning nearby Wi-Fi access points...{Colors.ENDC}")
    wifi_output = ""
    try:
        res = subprocess.run(["termux-wifi-scaninfo"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0 and res.stdout.strip() and "[]" not in res.stdout:
            wifi_output = res.stdout
    except Exception:
        pass
        
    if not wifi_output:
        try:
            res = subprocess.run(["nmcli", "dev", "wifi"], capture_output=True, text=True, timeout=5)
            wifi_output = res.stdout
        except Exception:
            try:
                res = subprocess.run(["iw", "dev"], capture_output=True, text=True, timeout=5)
                wifi_output = res.stdout
            except Exception:
                pass
                
    if wifi_output.strip():
        print(wifi_output)
    else:
        print(f"{Colors.YELLOW}[-] Wi-Fi scan returned no data. (Tip: Install 'termux-api' package & app).{Colors.ENDC}")

    print("\n" + "=" * 60)
    print(f"{Colors.GREEN}[*] Scanning nearby Bluetooth devices...{Colors.ENDC}")
    bt_output = ""
    try:
        res = subprocess.run(["termux-bluetooth-devices"], capture_output=True, text=True, timeout=5)
        if res.returncode == 0 and res.stdout.strip() and "[]" not in res.stdout:
            bt_output = res.stdout
    except Exception:
        pass
        
    if not bt_output:
        try:
            res = subprocess.run(["hcitool", "scan"], capture_output=True, text=True, timeout=6)
            bt_output = res.stdout
        except Exception:
            pass
            
    if bt_output.strip():
        print(bt_output)
    else:
        print(f"{Colors.RED}[-] Bluetooth scan returned no data. Ensure Bluetooth is enabled.{Colors.ENDC}")
        
    log_scan_result("Wireless & BT Scanner", "Local Airspace", "Executed airspace scan via Termux API/binaries")
    input(f"{Colors.YELLOW}\nPress Enter to return to main menu...{Colors.ENDC}")


def handle_monitor_mode():
    """Hardware Tool 15: Toggle wireless interface monitor mode via airmon-ng or iwconfig."""
    clear_screen()
    print_tactical_header()
    print("=== WIRELESS MONITOR MODE MANAGER ===".center(60))
    print("-" * 60)
    
    if not require_root("Wireless interface monitor mode management"):
        return

    print(f"{Colors.BOLD}1.{Colors.ENDC} Check Wireless Interfaces (airmon-ng / iwconfig)")
    print(f"{Colors.BOLD}2.{Colors.ENDC} Enable Monitor Mode on Interface (e.g., wlan0)")
    print(f"{Colors.BOLD}3.{Colors.ENDC} Disable Monitor Mode")
    print(f"{Colors.RED}99. Back (b){Colors.ENDC}")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select option [1-3, or 99/b]: {Colors.ENDC}").strip().lower()
    if choice in ["99", "b", "back"]:
        return
    elif choice == "1":
        try:
            res = subprocess.run(["airmon-ng"], capture_output=True, text=True, check=True)
            print(res.stdout)
        except Exception:
            try:
                res = subprocess.run(["iwconfig"], capture_output=True, text=True, check=True)
                print(res.stdout)
            except Exception as e:
                print(f"{Colors.RED}[-] Wireless query failed: {e}{Colors.ENDC}")
    elif choice == "2":
        iface = input(f"{Colors.YELLOW}Enter interface name to put into monitor mode (e.g., wlan0): {Colors.ENDC}").strip()
        if iface:
            try:
                subprocess.run(["airmon-ng", "start", iface], check=True)
                print(f"{Colors.GREEN}\n[✔] Monitor mode enabled.{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.RED}[-] Failed to start monitor mode: {e}{Colors.ENDC}")
    elif choice == "3":
        iface = input(f"{Colors.YELLOW}Enter monitor interface name to stop (e.g., wlan0mon): {Colors.ENDC}").strip()
        if iface:
            try:
                subprocess.run(["airmon-ng", "stop", iface], check=True)
                print(f"{Colors.GREEN}\n[✔] Monitor mode stopped.{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.RED}[-] Failed to stop monitor mode: {e}{Colors.ENDC}")
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")


def handle_bluetooth_recon():
    """Tool: Bluetooth & BLE Airspace Mapping."""
    clear_screen()
    print_tactical_header()
    print("=== BLUETOOTH & BLE AIRSPACE RECON ===".center(60))
    print("-" * 60)
    print(f"{Colors.BOLD}1.{Colors.ENDC} Scan Classic Bluetooth Devices (hcitool scan)")
    print(f"{Colors.BOLD}2.{Colors.ENDC} Scan BLE Devices (bluetoothctl scan le)")
    print(f"{Colors.RED}99. Back (b){Colors.ENDC}")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select option [1-2, or 99/b]: {Colors.ENDC}").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    if choice == "1":
        print(f"{Colors.GREEN}\n[+] Scanning for classic Bluetooth devices...{Colors.ENDC}")
        try:
            res = subprocess.run(["hcitool", "scan"], capture_output=True, text=True, timeout=15)
            output = res.stdout if res.stdout else res.stderr
            clear_screen()
            print_tactical_header()
            print("=== CLASSIC BLUETOOTH SCAN RESULTS ===".center(60))
            print(output)
            log_scan_result("Bluetooth Scan", "Airspace", output)
        except Exception as e:
            print(f"{Colors.RED}[-] Bluetooth scan failed (ensure HCI interface is up): {e}{Colors.ENDC}")
            
    elif choice == "2":
        print(f"{Colors.GREEN}\n[+] Scanning BLE beacons and devices (10s timeout)...{Colors.ENDC}")
        try:
            res = subprocess.run(["bluetoothctl", "scan", "le"], capture_output=True, text=True, timeout=10)
            output = res.stdout
            clear_screen()
            print_tactical_header()
            print("=== BLE SCAN RESULTS ===".center(60))
            print(output)
            log_scan_result("BLE Scan", "Airspace", output)
        except Exception as e:
            print(f"{Colors.RED}[-] BLE scan failed: {e}{Colors.ENDC}")
            
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")


def handle_bluetooth_attacks():
    """Tool 14: Advanced Bluetooth Enumeration & L2CAP Stress Testing."""
    clear_screen()
    print_tactical_header()
    print("=== PAGE: BLUETOOTH ATTACK SUITE ===".center(60))
    print("-" * 60)
    print(f"{Colors.BOLD}1.{Colors.ENDC} Scan & Enumerate Device SDP Services (sdptool)")
    print(f"{Colors.BOLD}2.{Colors.ENDC} L2CAP Ping Flood / Stress Test (l2ping) {Colors.RED}[ROOT REQUIRED]{Colors.ENDC}")
    print(f"{Colors.RED}99. Back (b){Colors.ENDC}")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select option [1-2, or 99/b]: {Colors.ENDC}").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    target_mac = input(f"{Colors.YELLOW}Enter Target Bluetooth MAC Address (e.g., 00:11:22:33:44:55): {Colors.ENDC}").strip()
    if not target_mac:
        return
        
    if choice == "1":
        print(f"{Colors.GREEN}\n[+] Querying SDP records for {target_mac}...{Colors.ENDC}")
        try:
            res = subprocess.run(["sdptool", "browse", target_mac], capture_output=True, text=True, timeout=15)
            output = res.stdout if res.stdout else res.stderr
            clear_screen()
            print_tactical_header()
            print("=== SDP BROWSE RESULTS ===".center(60))
            print(output)
            log_scan_result("Bluetooth SDP Browse", target_mac, output)
        except Exception as e:
            print(f"{Colors.RED}[-] SDP browse failed: {e}{Colors.ENDC}")
            
    elif choice == "2":
        if not require_root("Bluetooth L2CAP raw packet stress testing (l2ping)"):
            return
            
        count = input(f"{Colors.YELLOW}Enter packet count (default 500): {Colors.ENDC}").strip() or "500"
        print(f"{Colors.GREEN}\n[+] Executing l2ping stress test against {target_mac} ({count} packets)...{Colors.ENDC}")
        try:
            res = subprocess.run(["l2ping", "-i", "hci0", "-s", "600", "-c", count, target_mac], capture_output=True, text=True, timeout=20)
            output = res.stdout
            clear_screen()
            print_tactical_header()
            print("=== L2PING STRESS TEST RESULTS ===".center(60))
            print(output)
            log_scan_result("Bluetooth l2ping", target_mac, output)
        except Exception as e:
            print(f"{Colors.RED}[-] l2ping attack failed: {e}{Colors.ENDC}")
            
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")
