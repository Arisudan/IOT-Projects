#include <Wire.h>
#include "RTClib.h"

RTC_DS3231 rtc;

const int buzzerPin = 27;
const int snoozeButtonPin = 14;
const int acknowledgeButtonPin = 12;

struct ReminderTime {
  int hour;
  int minute;
  const char* medicineName;
};

ReminderTime schedule[] = {
  {8, 0, "Morning Dose"},
  {13, 0, "Afternoon Dose"},
  {20, 0, "Night Dose"}
};

const int reminderCount = sizeof(schedule) / sizeof(schedule[0]);
bool reminderActive = false;
int activeReminderIndex = -1;
unsigned long snoozeUntil = 0;

void setBuzzer(bool state) {
  digitalWrite(buzzerPin, state ? HIGH : LOW);
}

void triggerReminder(int index) {
  reminderActive = true;
  activeReminderIndex = index;
  Serial.print("Reminder: ");
  Serial.println(schedule[index].medicineName);
}

void stopReminder() {
  reminderActive = false;
  activeReminderIndex = -1;
  snoozeUntil = 0;
  setBuzzer(false);
}

void reminderTask(void* parameter) {
  for (;;) {
    DateTime now = rtc.now();

    if (!reminderActive && millis() >= snoozeUntil) {
      for (int i = 0; i < reminderCount; i++) {
        if (now.hour() == schedule[i].hour && now.minute() == schedule[i].minute && now.second() < 5) {
          triggerReminder(i);
          break;
        }
      }
    }

    if (reminderActive) {
      setBuzzer((millis() / 500) % 2);
    }

    vTaskDelay(pdMS_TO_TICKS(500));
  }
}

void inputTask(void* parameter) {
  for (;;) {
    if (digitalRead(acknowledgeButtonPin) == LOW) {
      Serial.println("Reminder acknowledged.");
      stopReminder();
      vTaskDelay(pdMS_TO_TICKS(600));
    }

    if (digitalRead(snoozeButtonPin) == LOW && reminderActive) {
      snoozeUntil = millis() + 5UL * 60UL * 1000UL;
      Serial.println("Reminder snoozed for 5 minutes.");
      stopReminder();
      vTaskDelay(pdMS_TO_TICKS(600));
    }

    vTaskDelay(pdMS_TO_TICKS(100));
  }
}

void displayTask(void* parameter) {
  for (;;) {
    DateTime now = rtc.now();
    Serial.printf("%02d:%02d:%02d | %s\n",
                  now.hour(), now.minute(), now.second(),
                  reminderActive ? schedule[activeReminderIndex].medicineName : "No active reminder");
    vTaskDelay(pdMS_TO_TICKS(1000));
  }
}

void setup() {
  Serial.begin(115200);
  Wire.begin();

  pinMode(buzzerPin, OUTPUT);
  pinMode(snoozeButtonPin, INPUT_PULLUP);
  pinMode(acknowledgeButtonPin, INPUT_PULLUP);

  if (!rtc.begin()) {
    Serial.println("RTC not found");
    while (true) {
      delay(1000);
    }
  }

  if (rtc.lostPower()) {
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
  }

  xTaskCreatePinnedToCore(reminderTask, "ReminderTask", 4096, nullptr, 1, nullptr, 1);
  xTaskCreatePinnedToCore(inputTask, "InputTask", 3072, nullptr, 1, nullptr, 1);
  xTaskCreatePinnedToCore(displayTask, "DisplayTask", 3072, nullptr, 1, nullptr, 1);
}

void loop() {
  delay(1000);
}