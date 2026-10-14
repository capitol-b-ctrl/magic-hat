# Magic Hat 🎩✨

​Magic Hat is an interactive command-line interface (CLI) tool built for Android/Termux environments. It combines a local item/budget inventory manager with a powerful penetration testing recon suite—complete with real-time network interface monitoring and automatic SQLite database logging.
​Features
​🌐 Dynamic Network Telemetry: Automatically detects and displays all active network interfaces and IP addresses (wlan0, rmnet0, etc.).
​🛡️ Nmap Recon Suite: Interactive scanning profiles (Quick, Service Version, Aggressive, and Custom flags) with real-time output display.
​💾 Persistent SQLite Storage: Automatically logs all scan outputs with timestamps and manages local props/budget inventories in ~/.magic_hat.db.
​🎨 Immersive CLI Experience: Clean ANSI-compatible terminal UI with custom ASCII art banners and buffer cleanup.
​Installation & Setup (Termux)
​Ensure your Termux environment has the necessary system binaries installed:

pkg update && pkg upgrade
pkg install python nmap iproute2 git

Clone your repository and install the package in editable mode:

git clone https://github.com/capitol-b-ctrl/magic-hat.git
cd Magic_Hat
pip install -e .


How to Open & Run
​Once installed, you can launch the tool from any directory in your terminal by typing:

magic-hat


Usage Guide
​Upon launching magic-hat, the main menu will display your active local network interfaces, IPs, and operational choices:
​Add a new prop or item: Log a new item name, estimated/actual price, and supplier into your local database.
​List all items in the Hat: Inspect all stored inventory items formatted neatly into a table.
​Search for an item: Perform keyword searches across your inventory items and suppliers.
​Show total acquisition budget: Automatically calculate and display the total financial cost of all tracked components.
​Run Nmap Recon: Enter a target IP, hostname, or CIDR block, select your scan profile, and stream results while saving them directly into your local SQLite log archive.
​Exit: Cleanly shut down the application session.

---

## 📂 Project Structure

```text
Magic_Hat/
├── .venv/                  # Isolated virtual environment (ignored by Git)
├── .gitignore              # Tells Git which files to ignore
├── README.md               # Project overview, setup, and instructions
├── pyproject.toml          # Modern central configuration for tools & dependencies
├── src/                    # Source code layout
│   └── magic_hat/          # Primary application package
│       ├── __init__.py     # Marks directory as an importable package
|	|── magic-hat.db    # Sqlite Database file for memory persistance
│       ├── magic-hat.py    # Primary entry point script
│       ├── database.py     # Sub-module for data handling
│       └── utils.py        # Sub-module for helper functions
└── tests/                  # Mirror of src/ used for automated testing
    ├── __init__.py
    └── test_database.py    # Unit tests targeting database logic

