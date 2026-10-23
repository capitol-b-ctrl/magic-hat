# MAGIC HAT // Tactical Red-Team & Security Auditing Framework

**Magic Hat** is a professional-grade, field-deployable security reconnaissance and auditing framework optimized for mobile environments (Termux), headless edge hardware, and tactical engagements. It provides a structured 12-phase lifecycle workflow, real-time structured SQLite telemetry, high-contrast terminal styling, and a built-in Flask web command center.

---

## 🚀 Key Features

* **12-Phase Security Auditing Lifecycle:** Standardized workflows covering Scope & Airspace Recon, Active Discovery, Vulnerability Analysis, Auto-Pilot Pipelines, Telemetry, and Reporting.
* **Centralized Configuration (`config.json`):** Easily modify default subnets, wordlists, server hosts, and binary parameters without modifying source code.
* **Pre-Flight Dependency Verification (`--check-deps`):** Automatically inspects `$PATH` for essential binaries (`nmap`, `tshark`, `ffuf`, `dig`, `searchsploit`, `pwsh`, `ssh`) before execution.
* **Headless Field Automation (`--headless`):** Run background reconnaissance scans against custom CIDR ranges directly from cron jobs or headless hardware implants.
* **Structured SQLite Telemetry:** Automatically logs raw tool outputs alongside parsed metadata (open ports, OS detection, MAC addresses, and vendor strings).
* **Matrix Terminal Web Command Center:** A responsive, pure black and neon-green Flask dashboard featuring live statistics, dynamic table filtering, and modal telemetry inspectors.
* **Comprehensive Tool Suite:** Includes Nmap deep profiling, packet capture (`tshark`), web fuzzing (`ffuf`), DNS footprinting, Exploit-DB searches (`searchsploit`), SSH remote auditing, PowerShell Core/WinRM management, and wireless monitor mode tools.
* **Automated Report Generator:** One-click export of engagement logs into structured Markdown (`.md`) and JSON summary reports.

## 🚀 Expanded Tactical Modules
* **Cryptographic Engine:** Built-in Base64 encoding/decoding and XOR stream obfuscation.
* **Payload Generator:** Instant generation of Python3, Bash, and Netcat reverse shell stubs mapped to custom LHOST/LPORT parameters.
* **QR Code Exploit Vector:** On-the-fly ASCII QR code rendering for malicious URLs and phishing redirection targets directly in the terminal.
* **Bluetooth Attack & Airspace Suite:** Classic Bluetooth SDP device browsing and L2CAP packet stress-testing (`l2ping`).

---

## 📂 Project Architecture

```text
Magic_Hat/
├── .git/
├── .gitignore
├── .venv/
├── .ruff_cache/
├── README.md
├── pyproject.toml
├── setup.py
├── src/
│   ├── command_not_found_handle
│   ├── magic-hat.py
│   ├── magic_hat.egg-info/
│   └── magic_hat/
│       ├── .ruff_cache/
│       ├── __init__.py
│       ├── __pycache__/
│       ├── config.json
│       ├── data/
│       │   └── magic_hat.db
│       ├── database.py
│       ├── main.py
│       ├── pipeline.py
│       ├── reports/
│       ├── reports.py
│       ├── server.py
│       ├── tools.py
│       └── utils.py
└── tests/
    ├── __init__.py
    └── test_database.py
```


## ⚙️ Installation & Setup
 * Clone the Repository:
   git clone [https://github.com/YOUR_USERNAME/Magic_Hat.git](https://github.com/YOUR_USERNAME/Magic_Hat.git)
cd Magic_Hat

 * Install in Editable Mode:
   pip install -e .

 * Install Core System Dependencies (Termux/Linux):
   pkg update && pkg install nmap tshark ffuf bind dnsutils git python libxml2 libxslt

 * Verify Environment Health:
   magic-hat --check-deps

## 🕹️ Usage & Execution
1. Interactive Tactical Menu
Launch the main framework interface:
magic-hat

2. Headless Recon Mode
Run automated subnet sweeps without launching the interactive UI:
magic-hat --headless --target 192.168.1.0/24

3. Web Command Center
From the interactive menu, select Phase 5 to toggle the local web server, then open your browser at:
👉 http://127.0.0.1:8080

## 📋 Security Auditing Lifecycle Phases

* **Phase 1: Offensive & Tactical Deployment Suite** — Access Nmap profilers, packet sniffers (`tshark`), web fuzzers (`ffuf`), DNS footprinting, reverse shell generators, QR vectors, and Bluetooth attack tools.
* **Phase 2: Network Mapping & Subnet Discovery** — ARP and ping sweeps across local and custom CIDR ranges.
* **Phase 3: Vulnerability & Service Audit Suite** — Multi-protocol credential auditing with Hydra.
* **Phase 4: Wireless & Airspace Intelligence** — Wi-Fi network scanning, BLE beacons, and RF recon.
* **Phase 5: Flask Web Dashboard Control** — Start/stop the background matrix command center and log viewer at `http://127.0.0.1:8080`.
* **Phase 6: Global Target Scope Manager** — Lock or clear active targets across all framework modules.
* **Phase 7: Binary Health Diagnostics** — Pre-flight inspection of required system binaries and packages.
* **Phase 8: Webhook / Notification Hub** — Outbound alert webhooks (Discord / Telegram) for scan status notifications.
* **Phase 9: Operator Quick-Shell Launcher** — Fast terminal escape shell for direct system commands.
* **Phase 10: Scan Archives & Telemetry Logs** — Interactive terminal browser for all recorded scans.
* **Phase 11: Tactical Report Generation** — One-click export to Markdown (`.md`) and JSON format, plus database purge options.
* **Phase 12: Automated Remote Telemetry Agent** — SSH into edge hardware (e.g. GL.iNet / OpenWrt routers) to gather board and system telemetry.

