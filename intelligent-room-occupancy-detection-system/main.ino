#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

const int pirPin = 27;
const int ledPin = 2;
const int buzzerPin = 4;

WebServer server(80);
bool roomOccupied = false;
unsigned long lastMotionTime = 0;
const unsigned long vacancyDelayMs = 15000;

String buildPage() {
  String page = "<!DOCTYPE html><html><head><meta name='viewport' content='width=device-width,initial-scale=1'>";
  page += "<style>body{font-family:Arial;background:#eef2ff;color:#111827;padding:24px;}";
  page += ".card{max-width:500px;background:#fff;padding:24px;border-radius:16px;box-shadow:0 10px 30px rgba(0,0,0,.08);}h1{margin-top:0;}</style></head><body>";
  page += "<div class='card'><h1>Room Occupancy</h1>";
  page += "<p><strong>Status:</strong> ";
  page += roomOccupied ? "Occupied" : "Empty";
  page += "</p><p>Refresh the page to see the latest room state.</p></div></body></html>";
  return page;
}

void handleRoot() {
  server.send(200, "text/html", buildPage());
}

void setup() {
  Serial.begin(115200);
  pinMode(pirPin, INPUT);
  pinMode(ledPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.print("Connecting");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print('.');
  }

  Serial.println();
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.begin();
}

void loop() {
  if (digitalRead(pirPin) == HIGH) {
    roomOccupied = true;
    lastMotionTime = millis();
    digitalWrite(ledPin, HIGH);
    digitalWrite(buzzerPin, HIGH);
  }

  if (roomOccupied && millis() - lastMotionTime > vacancyDelayMs) {
    roomOccupied = false;
    digitalWrite(ledPin, LOW);
    digitalWrite(buzzerPin, LOW);
  }

  server.handleClient();
  delay(100);
}
