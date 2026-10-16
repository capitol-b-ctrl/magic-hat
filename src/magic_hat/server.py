"""Flask background web dashboard and REST API for Magic Hat telemetry."""

import time
import json
import threading
import subprocess
from flask import Flask, render_template_string, jsonify, request
from magic_hat.database import get_scan_logs, get_connection
from magic_hat.utils import load_config

app = Flask(__name__)
server_thread = None
running = False

DASHBOARD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MAGIC HAT // Tactical Dashboard</title>
    <style>
        :root {
            --bg-color: #000000;
            --card-bg: #050a05;
            --border-color: #00ff66;
            --text-color: #00ff66;
            --text-dim: #00aa44;
            --glow-color: rgba(0, 255, 102, 0.4);
        }
        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            font-family: 'Courier New', Courier, monospace;
            margin: 0;
            padding: 20px;
            text-shadow: 0 0 2px var(--glow-color);
        }
        .header {
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 15px;
            margin-bottom: 25px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 4px 10px -5px var(--glow-color);
        }
        .header h1 {
            margin: 0;
            color: var(--text-color);
            font-size: 1.8rem;
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }
        .stat-card {
            background: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 4px;
            padding: 15px;
            text-align: center;
            box-shadow: inset 0 0 8px rgba(0, 255, 102, 0.1);
        }
        .stat-card .value {
            font-size: 2.2rem;
            color: var(--text-color);
            font-weight: bold;
        }
        .stat-card .label {
            font-size: 0.85rem;
            color: var(--text-dim);
            text-transform: uppercase;
            margin-top: 5px;
            letter-spacing: 1px;
        }
        .search-bar {
            width: 100%;
            padding: 12px;
            background: #000000;
            border: 1px solid var(--border-color);
            color: var(--text-color);
            border-radius: 4px;
            margin-bottom: 20px;
            font-family: inherit;
            box-sizing: border-box;
            outline: none;
        }
        .search-bar:focus {
            box-shadow: 0 0 8px var(--border-color);
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: var(--card-bg);
            border-radius: 4px;
            overflow: hidden;
            border: 1px solid var(--border-color);
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid rgba(0, 255, 102, 0.2);
        }
        th {
            background-color: #031508;
            color: var(--text-color);
            text-transform: uppercase;
            font-size: 0.85rem;
            letter-spacing: 1px;
        }
        tr:hover {
            background-color: #08200d;
        }
        .badge {
            background: rgba(0, 255, 102, 0.15);
            color: var(--text-color);
            padding: 3px 8px;
            border-radius: 3px;
            border: 1px solid var(--border-color);
            font-size: 0.8rem;
            font-weight: bold;
        }
        .modal {
            display: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(0,0,0,0.92);
            justify-content: center;
            align-items: center;
        }
        .modal-content {
            background: #000000;
            border: 2px solid var(--border-color);
            padding: 20px;
            width: 85%;
            max-width: 850px;
            max-height: 80vh;
            overflow-y: auto;
            border-radius: 4px;
            box-shadow: 0 0 20px var(--glow-color);
        }
        pre {
            background: #020803;
            padding: 15px;
            border: 1px solid rgba(0, 255, 102, 0.3);
            border-radius: 4px;
            color: var(--text-color);
            white-space: pre-wrap;
            word-break: break-all;
            font-size: 0.9rem;
        }
        .close-btn {
            background: var(--border-color);
            color: #000000;
            border: none;
            padding: 8px 16px;
            cursor: pointer;
            font-weight: bold;
            float: right;
            border-radius: 3px;
            font-family: inherit;
        }
        .close-btn:hover {
            box-shadow: 0 0 10px var(--border-color);
        }
        .action-btn {
            background: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-color);
            cursor: pointer;
            padding: 4px 10px;
            border-radius: 3px;
            font-family: inherit;
        }
        .action-btn:hover {
            background: var(--border-color);
            color: #000000;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>MAGIC HAT // TELEMETRY COMMAND CENTER</h1>
        <span class="badge">SYSTEM ONLINE</span>
    </div>

    <div class="stats-grid">
        <div class="stat-card">
            <div class="value" id="total-scans">{{ logs|length }}</div>
            <div class="label">Total Scan Archives</div>
        </div>
        <div class="stat-card">
            <div class="value" id="unique-targets">{{ unique_targets }}</div>
            <div class="label">Unique Targets</div>
        </div>
        <div class="stat-card">
            <div class="value">ONLINE</div>
            <div class="label">Server Status</div>
        </div>
    </div>

    <input type="text" id="search" class="search-bar" placeholder="Filter logs by tool name, target IP, or timestamp..." onkeyup="filterTable()">

    <table id="logs-table">
        <thead>
            <tr>
                <th>ID</th>
                <th>Tool Module</th>
                <th>Target Space</th>
                <th>Timestamp</th>
                <th>Action</th>
            </tr>
        </thead>
        <tbody>
            {% for log in logs %}
            <tr>
                <td>{{ log.id }}</td>
                <td><span class="badge">{{ log.tool_name }}</span></td>
                <td>{{ log.target }}</td>
                <td>{{ log.timestamp }}</td>
                <td><button class="action-btn" onclick="viewLog({{ log.id }})">View Telemetry</button></td>
            </tr>
            {% endfor %}
        </tbody>
    </table>

    <div id="log-modal" class="modal">
        <div class="modal-content">
            <button class="close-btn" onclick="closeModal()">CLOSE</button>
            <h2 id="modal-title" style="color: var(--text-color); margin-top: 0;"></h2>
            <p id="modal-target" style="color: var(--text-dim);"></p>
            <pre id="modal-output"></pre>
        </div>
    </div>

    <script>
        function filterTable() {
            let input = document.getElementById('search').value.toLowerCase();
            let rows = document.querySelectorAll('#logs-table tbody tr');
            rows.forEach(row => {
                let text = row.innerText.toLowerCase();
                row.style.display = text.includes(input) ? '' : 'none';
            });
        }

        function viewLog(id) {
            fetch('/api/logs/' + id)
                .then(res => res.json())
                .then(data => {
                    if(data.error) return alert(data.error);
                    document.getElementById('modal-title').innerText = '> ' + data.tool_name + ' TELEMETRY';
                    document.getElementById('modal-target').innerText = 'Target: ' + data.target + ' | Time: ' + data.timestamp;
                    document.getElementById('modal-output').innerText = data.output;
                    document.getElementById('log-modal').style.display = 'flex';
                });
        }

        function closeModal() {
            document.getElementById('log-modal').style.display = 'none';
        }
    </script>
</body>
</html>
"""


@app.route('/api/stream')
def api_stream():
    """Stream live telemetry events to the web dashboard in real-time."""
    def event_stream():
        last_id = 0
        while True:
            logs = get_scan_logs()
            if logs and logs[0]['id'] > last_id:
                latest = logs[0]
                last_id = latest['id']
                yield f"data: {json.dumps(latest)}\n\n"
            time.sleep(2)
    return app.response_class(event_stream(), mimetype='text/event-stream')

@app.route('/')
def index():
    logs = get_scan_logs()
    targets = set(l['target'] for l in logs)
    return render_template_string(DASHBOARD_HTML, logs=logs, unique_targets=len(targets))

@app.route('/api/logs/<int:log_id>')
def api_get_log(log_id):
    with get_connection() as conn:
        row = conn.execute("SELECT tool_name, target, timestamp, output, metadata_json FROM scan_logs WHERE id = ?", (log_id,)).fetchone()
        if row:
            return jsonify(dict(row))
        return jsonify({"error": "Log ID not found"}), 404

def run_server():
    config = load_config()
    host = config.get("server_host", "127.0.0.1")
    port = config.get("server_port", 8080)
    app.run(host=host, port=port, debug=False, use_reloader=False)

def toggle_web_server():
    global server_thread, running
    import magic_hat.utils as utils
    config = load_config()
    host = config.get("server_host", "127.0.0.1")
    port = config.get("server_port", 8080)

    if running:
        print("\n[*] Web dashboard is already running in the background.")
    else:
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        running = True
        utils.WEB_SERVER_ACTIVE = True
        print(f"\n[✔] Tactical Web Dashboard launched at http://{host}:{port}")
    
    # Return immediately to main menu without blocking input
    import time
    time.sleep(1.2)

def is_server_running():
    return running
    
    
    
    
    