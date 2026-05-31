#include <ESP32Servo.h>

const int waterLevelPin = 34;
const int temperaturePin = 35;
const int feederServoPin = 13;
const int pumpRelayPin = 26;
const int buzzerPin = 27;

ESP32Servo feederServo;

const int lowWaterThreshold = 1400;
const int highWaterThreshold = 3000;
const int feedingHour = 9;
const int cleaningHour = 18;
bool feedingDoneToday = false;
bool cleaningDoneToday = false;
int lastDay = -1;

float readTemperatureCelsius() {
  int raw = analogRead(temperaturePin);
  return (raw / 4095.0) * 50.0;
}

void dispenseFood() {
  feederServo.write(90);
  delay(800);
  feederServo.write(0);
  Serial.println("Food dispensed.");
}

void runCleaningCycle() {
  digitalWrite(pumpRelayPin, HIGH);
  delay(5000);
  digitalWrite(pumpRelayPin, LOW);
  Serial.println("Cleaning cycle completed.");
}

void alertUser(const char* message) {
  Serial.println(message);
  digitalWrite(buzzerPin, HIGH);
  delay(200);
  digitalWrite(buzzerPin, LOW);
}

void setup() {
  Serial.begin(115200);

  pinMode(pumpRelayPin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);
  digitalWrite(pumpRelayPin, LOW);

  feederServo.attach(feederServoPin);
  feederServo.write(0);
}

void loop() {
  int waterLevel = analogRead(waterLevelPin);
  float temperature = readTemperatureCelsius();
  unsigned long seconds = millis() / 1000UL;
  int currentHour = (seconds / 3600UL) % 24;
  int currentDay = (seconds / 86400UL) % 31;

  if (currentDay != lastDay) {
    feedingDoneToday = false;
    cleaningDoneToday = false;
    lastDay = currentDay;
  }

  Serial.print("Water level: ");
  Serial.print(waterLevel);
  Serial.print(" | Temp: ");
  Serial.println(temperature);

  if (waterLevel < lowWaterThreshold) {
    alertUser("Water level low");
  }

  if (waterLevel > highWaterThreshold) {
    alertUser("Water level high");
  }

  if (!feedingDoneToday && currentHour == feedingHour) {
    dispenseFood();
    feedingDoneToday = true;
  }

  if (!cleaningDoneToday && currentHour == cleaningHour) {
    runCleaningCycle();
    cleaningDoneToday = true;
  }

  delay(5000);
}