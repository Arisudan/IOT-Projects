from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import random
import threading
import time
from urllib.parse import urlparse

HOST = "127.0.0.1"
PORT = 8030

assets = [
    {"id": "A-101", "name": "Forklift Battery", "location": "Warehouse", "status": "Available"},
    {"id": "A-204", "name": "Safety Helmet Cart", "location": "Loading Dock", "status": "In Transit"},
    {"id": "A-311", "name": "Calibration Kit", "location": "Maintenance Room", "status": "Checked In"},
]

HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>IoT-Based Asset Tracking and Monitoring System</title>
  <style>
    body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#eff6ff,#f8fafc);margin:0;padding:24px;color:#111827}
    .wrap{max-width:1000px;margin:0 auto}
    .card{background:#fff;border-radius:18px;padding:20px;margin-bottom:16px;box-shadow:0 10px 30px rgba(0,0,0,.08)}
    table{width:100%;border-collapse:collapse}
    th,td{padding:12px;border-bottom:1px solid #e5e7eb;text-align:left}
    button{border:0;border-radius:10px;padding:10px 14px;cursor:pointer;background:#2563eb;color:#fff;margin-right:8px}
    button.secondary{background:#374151}
  </style>
</head>
<body>
  <div class='wrap'>
    <div class='card'>
      <h1>IoT-Based Asset Tracking and Monitoring System</h1>
      <p>Use the controls to simulate status updates for the demo dashboard.</p>
      <button onclick='shuffleAssets()'>Refresh Demo Movement</button>
      <button class='secondary' onclick='markWarehouse()'>Send All to Warehouse</button>
    </div>
    <div class='card'>
      <table>
        <thead><tr><th>ID</th><th>Name</th><th>Location</th><th>Status</th></tr></thead>
        <tbody id='rows'></tbody>
      </table>
    </div>
  </div>
<script>
async function refreshAssets() {
  const response = await fetch('/api/assets');
  const data = await response.json();
  const rows = document.getElementById('rows');
  rows.innerHTML = '';
  for (const asset of data) {
    rows.innerHTML += `<tr><td>${asset.id}</td><td>${asset.name}</td><td>${asset.location}</td><td>${asset.status}</td></tr>`;
  }
}

async function shuffleAssets() {
  await fetch('/api/action', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({action:'shuffle'})});
  refreshAssets();
}

async function markWarehouse() {
  await fetch('/api/action', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({action:'warehouse'})});
  refreshAssets();
}

refreshAssets();
setInterval(refreshAssets, 4000);
</script>
</body>
</html>
"""


def mutate_assets(action: str) -> None:
    locations = ["Warehouse", "Loading Dock", "Maintenance Room", "Delivery Truck", "Service Bay"]
    statuses = ["Available", "In Transit", "Checked In", "On Route"]
    if action == "warehouse":
        for asset in assets:
            asset["location"] = "Warehouse"
            asset["status"] = "Available"
        return

    for asset in assets:
        asset["location"] = random.choice(locations)
        asset["status"] = random.choice(statuses)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/assets':
            payload = json.dumps(assets).encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return

        page = HTML_PAGE.encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(page)))
        self.end_headers()
        self.wfile.write(page)

    def do_POST(self):
        if urlparse(self.path).path != '/api/action':
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get('Content-Length', '0'))
        body = self.rfile.read(length).decode('utf-8')
        try:
            action = json.loads(body).get('action', 'shuffle')
        except json.JSONDecodeError:
            action = 'shuffle'

        mutate_assets(action)
        payload = json.dumps({'ok': True}).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def background_updates() -> None:
    while True:
        mutate_assets('shuffle')
        time.sleep(5)


def main() -> None:
    threading.Thread(target=background_updates, daemon=True).start()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f'Open http://{HOST}:{PORT} in your browser')
    server.serve_forever()


if __name__ == '__main__':
    main()
