## Magic Hat 🎩✨

​Magic Hat is an interactive command-line interface (CLI) tool built for Android/Termux environments. It combines a local item/budget inventory manager with a powerful penetration testing recon suite—complete with real-time network interface monitoring and automatic SQLite database logging.
​Features
​🌐 Dynamic Network Telemetry: Automatically detects and displays all active network interfaces and IP addresses (wlan0, rmnet0, etc.).
​🛡️ Nmap Recon Suite: Interactive scanning profiles (Quick, Service Version, Aggressive, and Custom flags) with real-time output display.
​💾 Persistent SQLite Storage: Automatically logs all scan outputs with timestamps and manages local props/budget inventories in ~/.magic_hat.db.
​🎨 Immersive CLI Experience: Clean ANSI-compatible terminal UI with custom ASCII art banners and buffer cleanup.
​Installation & Setup (Termux)# 🎩 Magic Hat: Mobile Offensive Security & Recon Suite

**Magic Hat** is a modular, mobile-first reconnaissance and penetration testing CLI framework optimized for **Termux** and **Kali NetHunter** environments. Built with a local SQLite telemetry backend, it streamlines field operations, automated tool execution, live network telemetry, and markdown report generation directly from your mobile device.

---

## 🚀 Key Features

* **Multi-Interface Network Intelligence:** Automatically detects and displays active IP addresses across all device network interfaces (e.g., Wi-Fi `wlan0`, cellular data `rmnet0`) in real time.
* **Persistent SQLite Telemetry (`~/.magic_hat.db`):** Automatically logs all tool outputs, targets, timestamps, and scan logs for historical review and tracking.
* **Interactive Scan Archives:** Browse, select, and review past scan outputs by incremental ID directly from the terminal.
* **Automated Reporting Engine:** Instantly compiles individual or full engagement logs into formatted Markdown intelligence reports saved to `~/magic_hat_reports/`.
* **Webhook Telemetry Hooks:** Supports optional notification triggers to pipe task completions and alerts to external or local endpoints.

---

## 🛠️ Integrated Security Suite

The built-in **Offensive Security Suite** features 8 modular operational tools:

1. **Nmap Recon Suite:** Multiple scan profiles (Quick, Top 100 Ports + Version Detection `-sV`, Full Port Sweep `-p-`, and Custom Flags) with built-in regex parsing that extracts open ports and services into clean summary tables.
2. **Net Shark (`tshark`):** Live packet capture and traffic analysis wrapper across selected mobile interfaces.
3. **Web Directory Fuzzer (`ffuf` / `gobuster`):** Web asset and hidden directory enumeration.
4. **DNS Footprinting (`dig`):** Domain record queries (A, MX, NS, ANY) and zone transfer checks (`AXFR`).
5. **Web Tech Fingerprint (`whatweb`):** Content management system, server, and technology stack identification.
6. **Subnet & ARP Discovery:** Live host mapping across local interfaces and target CIDRs.
7. **Wireless & RF Footprinting:** Wi-Fi network and adapter status inspection (`iw` / `nmcli`).
8. **Hash Identifier & Audit Engine:** Heuristic regex hash signature identification paired with a local `hashcat` password audit wrapper.

---

## 📦 Installation & Setup

### Prerequisites (Termux / NetHunter)
Ensure your mobile environment has the core utility binaries installed:
```bash
pkg update && pkg upgrade
pkg install python git nmap tshark dnsutils
```

Clone your repository and install the package in editable mode:

git clone https://github.com/capitol-b-ctrl/magic-hat.git
cd Magic_Hat
pip install -e .


How to Open & Run
​Once installed, you can launch the tool from any directory in your terminal by typing:

```text 
magic-hat
```

## 🕹️ Usage Guide

Launch the interactive **Magic Hat** CLI dashboard from anywhere in your mobile terminal:

```text
magic-hat
```

Main Menu Options

​When you start the application, it automatically detects and displays your active device network interfaces (e.g., Wi-Fi wlan0, cellular rmnet0) before presenting the primary menu:

​1. Add a new prop or item: Log equipment, hardware components, or tools into your local SQLite inventory with pricing and supplier details.
​2. List all items in the Hat: View a formatted table of all saved physical or digital assets.
​3. Search for an item: Query your local inventory archives by keyword.
​4. Show total acquisition budget: Calculate the total aggregate cost of all stored inventory components.
​5. Offensive Security Suite (Tools): Open the secondary security submenu containing 10 modular offensive tools:

    ​•Nmap Recon Suite (Quick, Version, Full Sweep, Custom flags with regex parsing)

    ​•Net Shark (tshark packet capture wrapper)

    ​•Web Directory Fuzzer (ffuf / gobuster)

    ​•DNS Footprinting (dig records & zone transfers)

    ​•Web Tech Fingerprint (whatweb)

    ​•Subnet & ARP Discovery

    ​•Wireless & RF Footprinting (iw / nmcli)

    ​•Hash Identifier & Audit Engine (hashcat assistant)

    ​•Exploit Search Engine (searchsploit)

    ​•Credential Auditor (hydra)

    ​•Automated Report Generator (Compile logs to Markdown)

​6. Auto-Pilot Recon Pipeline: Execute an automated chain that runs a version scan, tech fingerprinting, and compiles a complete report automatically.

​7. Launch Local Web Dashboard (Server): Spin up a self-hosted Flask web interface at http://127.0.0.1:8080 to view your telemetry live in any browser.

​8. View Scan Archives (Logs): Browse historical scan logs, inspect past targets, and read full terminal outputs by numeric ID.

​9. Exit: Safely shut down the session.

Pro-Tips for Field Operations

      ●​**Automated Reports:** Whenever you run tool scans, you can export them directly into clean Markdown files located in your local src/magic_hat/reports/ folder.

      ●**Database Telemetry:** All scan results and inventory data are safely enclosed inside src/magic_hat/data/magic_hat.db.


## 📂 Project Structure


``` text
Magic_Hat/
├── .venv/                  # Isolated virtual environment (ignored by Git)
├── .gitignore              # Tells Git which files to ignore
├── README.md               # Project overview, setup, and instructions
├── pyproject.toml          # Modern central configuration for tools & dependencies
├── src/                    # Source code layout
│   └── magic_hat/          # Primary application package
│       ├── __init__.py
│       ├── main.py       # Main CLI loop, banner, and interface routing
│       ├── database.py   # SQLite schema and telemetry logging
│       ├── tools.py      # Offensive security tool wrappers & regex parsers
│       ├── reports.py    # Automated Markdown engagement report generator
│       ├── pipeline.py   # Automated multi-tool recon execution chain
│       ├── server.py     # Local Flask web dashboard and API server
│       ├── utils.py      # System helpers, dynamic IP detection, and webhooks
│       ├── data/         # Local enclosed database directory
│       │   └── magic_hat.db
│       └── reports/      # Local enclosed Markdown engagement reports
├── tests/                  # Mirror of src/ used for automated testing
│   ├── __init__.py
│   └── test_database.py    # Unit tests targeting database │
└── setup.py                # Package installation script
 

