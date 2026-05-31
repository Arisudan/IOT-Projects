from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import random
import threading
import time
from urllib.parse import urlparse

HOST = "127.0.0.1"
PORT = 8010

state = {
    "machine_name": "Milling Machine A",
    "health": 92,
    "temperature": 61.2,
    "vibration": 1.8,
    "pressure": 2.4,
    "load": 67,
}

HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>Real-Time Machine Health Monitoring Platform</title>
  <style>
    body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#f8fafc,#eef2ff);margin:0;padding:24px;color:#111827}
    .wrap{max-width:960px;margin:0 auto}
    .card{background:#fff;border-radius:18px;padding:20px;margin-bottom:16px;box-shadow:0 10px 30px rgba(0,0,0,.08)}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:16px}
    .metric{font-size:2rem;font-weight:700}
    .muted{color:#6b7280}
  </style>
</head>
<body>
  <div class='wrap'>
    <div class='card'>
      <h1>Real-Time Machine Health Monitoring Platform</h1>
      <p class='muted'>The dashboard refreshes automatically every few seconds.</p>
    </div>
    <div class='grid'>
      <div class='card'><div class='muted'>Machine</div><div class='metric' id='machine_name'></div></div>
      <div class='card'><div class='muted'>Health</div><div class='metric' id='health'></div></div>
      <div class='card'><div class='muted'>Temperature</div><div class='metric' id='temperature'></div></div>
      <div class='card'><div class='muted'>Vibration</div><div class='metric' id='vibration'></div></div>
      <div class='card'><div class='muted'>Pressure</div><div class='metric' id='pressure'></div></div>
      <div class='card'><div class='muted'>Load</div><div class='metric' id='load'></div></div>
    </div>
  </div>
<script>
async function refreshState() {
  const response = await fetch('/api/state');
  const data = await response.json();
  for (const [key, value] of Object.entries(data)) {
    const element = document.getElementById(key);
    if (element) {
      element.textContent = typeof value === 'number' ? value.toFixed ? value.toFixed(1) : value : value;
    }
  }
}
refreshState();
setInterval(refreshState, 3000);
</script>
</body>
</html>
"""


def update_state() -> None:
    while True:
        state["temperature"] = round(58 + random.uniform(-2, 8), 1)
        state["vibration"] = round(max(0.2, random.uniform(0.5, 3.5)), 2)
        state["pressure"] = round(random.uniform(1.8, 3.8), 2)
        state["load"] = max(0, min(100, state["load"] + random.randint(-4, 4)))
        state["health"] = max(0, min(100, 100 - int((state["temperature"] - 55) * 2) - int(state["vibration"] * 6)))
        time.sleep(2)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/state':
            payload = json.dumps(state).encode('utf-8')
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


def main() -> None:
    threading.Thread(target=update_state, daemon=True).start()
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f'Open http://{HOST}:{PORT} in your browser')
    server.serve_forever()


if __name__ == '__main__':
    main()
