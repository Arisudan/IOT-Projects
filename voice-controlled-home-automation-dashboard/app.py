import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000

state = {
    "living_room_light": "OFF",
    "fan": "OFF",
    "tv": "OFF",
}

HTML_PAGE = """<!DOCTYPE html>
<html>
<head>
  <meta name='viewport' content='width=device-width, initial-scale=1'>
  <title>Voice-Controlled Home Automation Dashboard</title>
  <style>
    body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#eef2ff,#f8fafc);margin:0;padding:24px;color:#111827}
    .wrap{max-width:900px;margin:0 auto}
    .card{background:#fff;border-radius:18px;padding:20px;margin-bottom:16px;box-shadow:0 10px 30px rgba(0,0,0,.08)}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:16px}
    button{border:0;border-radius:12px;padding:12px 16px;cursor:pointer;background:#2563eb;color:#fff}
    button.secondary{background:#374151}
    .status{font-weight:bold}
    .muted{color:#6b7280}
  </style>
</head>
<body>
  <div class='wrap'>
    <div class='card'>
      <h1>Voice-Controlled Home Automation Dashboard</h1>
      <p class='muted'>Use the buttons or your browser microphone to control devices.</p>
      <p class='muted'>If voice is not supported in your browser, you can still use the on-screen buttons or type a command.</p>
      <button onclick='startVoice()'>Start Voice Control</button>
      <button class='secondary' onclick='allOff()'>Turn All Off</button>
      <div style='margin-top:12px'>
        <input id='manualCommand' placeholder='Type a command like fan on' style='padding:12px;border:1px solid #d1d5db;border-radius:12px;width:min(320px,100%);margin-right:8px' />
        <button class='secondary' onclick='sendManual()'>Send Command</button>
      </div>
      <p id='voiceResult' class='status'>Say: "light on", "fan off", or "all off"</p>
    </div>

    <div class='grid'>
      <div class='card'><h3>Living Room Light</h3><p id='living_room_light'>Loading...</p><button onclick='sendCommand("light on")'>ON</button> <button class='secondary' onclick='sendCommand("light off")'>OFF</button></div>
      <div class='card'><h3>Fan</h3><p id='fan'>Loading...</p><button onclick='sendCommand("fan on")'>ON</button> <button class='secondary' onclick='sendCommand("fan off")'>OFF</button></div>
      <div class='card'><h3>TV</h3><p id='tv'>Loading...</p><button onclick='sendCommand("tv on")'>ON</button> <button class='secondary' onclick='sendCommand("tv off")'>OFF</button></div>
    </div>
  </div>

<script>
let recognition;

async function refreshState() {
  const response = await fetch('/api/state');
  const data = await response.json();
  for (const key of Object.keys(data)) {
    const element = document.getElementById(key);
    if (element) {
      element.textContent = data[key];
    }
  }
}

async function sendCommand(command) {
  try {
    await fetch('/api/command', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({command})
    });
    refreshState();
  } catch (error) {
    document.getElementById('voiceResult').textContent = 'Could not send command.';
  }
}

function allOff() {
  sendCommand('all off');
}

function sendManual() {
  const input = document.getElementById('manualCommand');
  sendCommand(input.value || '');
  input.value = '';
}

function startVoice() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    document.getElementById('voiceResult').textContent = 'Speech recognition is not supported in this browser.';
    return;
  }

  recognition = new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.onresult = event => {
    const command = event.results[0][0].transcript.toLowerCase();
    document.getElementById('voiceResult').textContent = 'Heard: ' + command;
    sendCommand(command);
  };
  recognition.start();
}

refreshState();
setInterval(refreshState, 3000);
</script>
</body>
</html>
"""


def apply_command(command: str) -> None:
    command = command.lower().strip()
    if 'all off' in command:
        for key in state:
            state[key] = 'OFF'
    elif 'light on' in command:
        state['living_room_light'] = 'ON'
    elif 'light off' in command:
        state['living_room_light'] = 'OFF'
    elif 'fan on' in command:
        state['fan'] = 'ON'
    elif 'fan off' in command:
        state['fan'] = 'OFF'
    elif 'tv on' in command:
        state['tv'] = 'ON'
    elif 'tv off' in command:
        state['tv'] = 'OFF'


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

    def do_POST(self):
        if urlparse(self.path).path != '/api/command':
            self.send_response(404)
            self.end_headers()
            return

        length = int(self.headers.get('Content-Length', '0'))
        body = self.rfile.read(length).decode('utf-8')
        try:
            command = json.loads(body).get('command', '')
        except json.JSONDecodeError:
            command = ''

        apply_command(command)
        payload = json.dumps({'ok': True}).encode('utf-8')
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Voice-Controlled Home Automation Dashboard")
    parser.add_argument("--host", default=DEFAULT_HOST, help="Host to bind")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to bind")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f'Open http://{args.host}:{args.port} in your browser')
    print('Use the voice button or the on-screen controls.')
    server.serve_forever()


if __name__ == '__main__':
    main()
