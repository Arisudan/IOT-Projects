from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import random
import threading
import time
from urllib.parse import urlparse

HOST = "127.0.0.1"
PORT = 8020

state = {
    "output": 1240,
    "downtime": 18,
    "defects": 6,
    "efficiency": 91,
    "shift": "A",
}

HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>Factory Production Analytics Dashboard</title>
  <style>
    body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#f8fafc,#fff7ed);margin:0;padding:24px;color:#111827}
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
      <h1>Factory Production Analytics Dashboard</h1>
      <p class='muted'>Production metrics update automatically every few seconds.</p>
    </div>
    <div class='grid'>
      <div class='card'><div class='muted'>Shift</div><div class='metric' id='shift'></div></div>
      <div class='card'><div class='muted'>Output</div><div class='metric' id='output'></div></div>
      <div class='card'><div class='muted'>Downtime</div><div class='metric' id='downtime'></div></div>
      <div class='card'><div class='muted'>Defects</div><div class='metric' id='defects'></div></div>
      <div class='card'><div class='muted'>Efficiency</div><div class='metric' id='efficiency'></div></div>
    </div>
  </div>
<script>
async function refreshState() {
  const response = await fetch('/api/state');
  const data = await response.json();
  for (const [key, value] of Object.entries(data)) {
    const element = document.getElementById(key);
    if (element) {
      element.textContent = key === 'efficiency' ? value + '%' : value;
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
    shifts = ["A", "B", "C"]
    while True:
        state["shift"] = random.choice(shifts)
        state["output"] = max(800, min(1500, state["output"] + random.randint(-30, 35)))
        state["downtime"] = max(0, min(120, state["downtime"] + random.randint(-2, 4)))
        state["defects"] = max(0, min(40, state["defects"] + random.randint(-1, 2)))
        state["efficiency"] = max(0, min(100, 100 - state["downtime"] // 2 - state["defects"] * 2))
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
