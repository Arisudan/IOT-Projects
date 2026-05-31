#include <WiFi.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

const int slotCount = 4;
const int sensorPins[slotCount] = {32, 33, 25, 26};
const int ledPins[slotCount] = {16, 17, 18, 19};

WiFiServer server(80);

void updateSlotOutputs(const bool occupied[slotCount]) {
  for (int i = 0; i < slotCount; i++) {
    digitalWrite(ledPins[i], occupied[i] ? HIGH : LOW);
  }
}

String buildHtmlPage(const bool occupied[slotCount]) {
  int freeSlots = 0;
  String rows;

  for (int i = 0; i < slotCount; i++) {
    if (!occupied[i]) {
      freeSlots++;
    }
    rows += "<li>Slot ";
    rows += String(i + 1);
    rows += ": ";
    rows += occupied[i] ? String("Occupied") : String("Free");
    rows += "</li>";
  }

  String html = "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'>";
  html += "<style>body{font-family:Arial;margin:24px;background:#f5f7fb;color:#1f2937;}";
  html += ".card{max-width:520px;background:#fff;padding:24px;border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,.08);}li{margin:8px 0;}</style></head><body>";
  html += "<div class='card'><h1>Smart Car Parking IoT</h1>";
  html += "<p><strong>Free slots:</strong> ";
  html += String(freeSlots);
  html += " / ";
  html += String(slotCount);
  html += "</p><ul>";
  html += rows;
  html += "</ul><p>Refresh the page to see the latest status.</p></div></body></html>";
  return html;
}

void setup() {
  Serial.begin(115200);

  for (int i = 0; i < slotCount; i++) {
    pinMode(sensorPins[i], INPUT_PULLUP);
    pinMode(ledPins[i], OUTPUT);
    digitalWrite(ledPins[i], LOW);
  }

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.print("Connecting to Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print('.');
  }

  Serial.println();
  Serial.print("Connected. IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void loop() {
  bool occupied[slotCount];
  int freeSlots = 0;

  for (int i = 0; i < slotCount; i++) {
    occupied[i] = digitalRead(sensorPins[i]) == LOW;
    if (!occupied[i]) {
      freeSlots++;
    }
  }

  updateSlotOutputs(occupied);

  Serial.print("Free slots: ");
  Serial.println(freeSlots);

  WiFiClient client = server.available();
  if (client) {
    String request = client.readStringUntil('\r');
    client.flush();

    String response = buildHtmlPage(occupied);
    client.println("HTTP/1.1 200 OK");
    client.println("Content-Type: text/html");
    client.println("Connection: close");
    client.println();
    client.println(response);
    delay(1);
    client.stop();
  }

  delay(1000);
}