# MAGIC HAT // Tactical Red-Team & Security Auditing Framework

**Magic Hat** is a professional-grade, field-deployable security reconnaissance and auditing framework optimized for mobile environments (Termux), headless edge hardware, and tactical engagements. It provides a structured 6-phase lifecycle workflow, real-time structured SQLite telemetry, high-contrast terminal styling, and a built-in Flask web command center.

---

## 🚀 Key Features

* **6-Phase Security Auditing Lifecycle:** Standardized workflows covering Scope & Airspace Recon, Active Discovery, Vulnerability Analysis, Auto-Pilot Pipelines, Telemetry, and Reporting.
* **Centralized Configuration (`config.json`):** Easily modify default subnets, wordlists, server hosts, and binary parameters without modifying source code.
* **Pre-Flight Dependency Verification (`--check-deps`):** Automatically inspects `$PATH` for essential binaries (`nmap`, `tshark`, `ffuf`, `dig`, `searchsploit`, `pwsh`, `ssh`) before execution.
* **Headless Field Automation (`--headless`):** Run background reconnaissance scans against custom CIDR ranges directly from cron jobs or headless hardware implants.
* **Structured SQLite Telemetry:** Automatically logs raw tool outputs alongside parsed metadata (open ports, OS detection, MAC addresses, and vendor strings).
* **Matrix Terminal Web Command Center:** A responsive, pure black and neon-green Flask dashboard featuring live statistics, dynamic table filtering, and modal telemetry inspectors.
* **Comprehensive Tool Suite:** Includes Nmap deep profiling, packet capture (`tshark`), web fuzzing (`ffuf`), DNS footprinting, Exploit-DB searches (`searchsploit`), SSH remote auditing, PowerShell Core/WinRM management, and wireless monitor mode tools.
* **Automated Report Generator:** One-click export of engagement logs into structured Markdown (`.md`) and JSON summary reports.

---

## 📂 Project Architecture

```text
Magic_Hat/
├── config.json                 # Centralized framework configuration
├── pyproject.toml              # Package configuration & entry points
└── src/
    └── magic_hat/
        ├── __init__.py
        ├── main.py             # CLI parser & 6-phase interactive menu loop
        ├── utils.py            # Helpers, banner art, IP detection, config loader
        ├── database.py         # SQLite telemetry storage & schema migrations
        ├── tools.py            # Offensive auditing suite (Nmap, SSH, PowerShell, etc.)
        ├── pipeline.py         # Multi-stage automated recon chains
        ├── server.py           # Flask web dashboard & REST API
        └── reports.py          # Markdown & JSON engagement report generator
```


⚙️ Installation & Setup
 * Clone the Repository:
   git clone [https://github.com/YOUR_USERNAME/Magic_Hat.git](https://github.com/YOUR_USERNAME/Magic_Hat.git)
cd Magic_Hat

 * Install in Editable Mode:
   pip install -e .

 * Install Core System Dependencies (Termux/Linux):
   pkg update && pkg install nmap tshark ffuf bind dnsutils git python libxml2 libxslt

 * Verify Environment Health:
   magic-hat --check-deps

🕹️ Usage & Execution
1. Interactive Tactical Menu
Launch the main framework interface:
magic-hat

2. Headless Recon Mode
Run automated subnet sweeps without launching the interactive UI:
magic-hat --headless --target 192.168.1.0/24

3. Web Command Center
From the interactive menu, select Phase 5 to toggle the local web server, then open your browser at:
👉 http://127.0.0.1:8080
📋 Security Auditing Lifecycle Phases
 * Phase 1: Scope & Airspace Recon — Wireless and Bluetooth interface management & monitor mode toggling.
 * Phase 2: Active Network Discovery — ARP and Ping subnet host sweeping.
 * Phase 3: Vulnerability & Service Audit Suite — Access Nmap deep profilers, SSH auditing, PowerShell Core/WinRM tools, Ffuf, and Exploit-DB searches.
 * Phase 4: Auto-Pilot Assessment Pipeline — Chained multi-stage background scans.
 * Phase 5: Telemetry Server — Real-time Flask command center and log browser.
 * Phase 6: Audit Archives & Reporting — Export clean Markdown and JSON engagement summaries.

