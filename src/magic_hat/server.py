"""Local web dashboard and API server for Magic Hat."""

import os
from flask import Flask, jsonify, render_template_string
from magic_hat.database import get_scan_logs, get_connection

app = Flask("magic_hat_server")

DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Magic Hat Web Dashboard</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { font-family: monospace; background: #121212; color: #00ff66; padding: 15px; margin: 0; }
        h1 { color: #ffffff; border-bottom: 2px solid #00ff66; padding-bottom: 10px; font-size: 1.4rem; }
        h2 { font-size: 1.1rem; color: #ff0055; margin-top: 20px; }
        .card { background: #1e1e1e; border: 1px solid #333; padding: 12px; margin-bottom: 12px; border-radius: 6px; }
        pre { background: #000000; padding: 10px; overflow-x: auto; color: #cccccc; font-size: 0.8rem; border-radius: 4px; }
        .badge { background: #00ff66; color: #000; padding: 2px 6px; font-size: 0.7rem; font-weight: bold; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>🎩 Magic Hat Dashboard</h1>
    <p>Mobile Operational Intelligence & Telemetry Server</p>
    
    <h2>Recent Scan Logs (Database Telemetry)</h2>
    {% for log in logs %}
    <div class="card">
        <span class="badge">ID: {{ log.id }}</span> <strong>{{ log.tool_name }}</strong><br>
        <strong>Target:</strong> {{ log.target }} | <small>{{ log.timestamp }}</small>
        <pre>{{ log.output[:1500] }}</pre>
    </div>
    {% endfor %}
</body>
</html>
"""

@app.route("/")
def index():
    with get_connection() as conn:
        logs = [dict(row) for row in conn.execute("SELECT * FROM scan_logs ORDER BY id DESC LIMIT 25").fetchall()]
    return render_template_string(DASHBOARD_TEMPLATE, logs=logs)

@app.route("/api/logs")
def api_logs():
    return jsonify(get_scan_logs())

def run_web_server(host="127.0.0.1", port=8080):
    print(f"[+] Starting Magic Hat Web Dashboard at http://{host}:{port}")
    print("[*] Press Ctrl+C in terminal to shut down the server.")
    app.run(host=host, port=port, debug=False)
