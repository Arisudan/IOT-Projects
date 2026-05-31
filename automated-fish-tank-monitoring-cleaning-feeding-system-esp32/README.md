# Automated Fish Tank Monitoring, Cleaning and Feeding System using ESP32

![ESP32](https://img.shields.io/badge/Board-ESP32-blue)
![Automation](https://img.shields.io/badge/Feature-Automated%20Maintenance-orange)
![IoT](https://img.shields.io/badge/Domain-IoT-green)
![Status](https://img.shields.io/badge/Status-Documentation%20Ready-brightgreen)

## Overview
This project automates aquarium monitoring and routine care with an ESP32. It tracks tank conditions, performs scheduled feeding, and can trigger cleaning or filtration actions to reduce manual effort.

## At a Glance
- Board: ESP32 development board
- Sensors: Water level, temperature, and optional pH or turbidity
- Actuators: Feeder motor, pump, relay, LEDs, buzzer
- Output: LCD/OLED display and optional web dashboard

## Problem Statement
Aquariums need regular attention, but manual monitoring can miss issues like low water, overfeeding, or poor water quality. This project automates the routine checks and actions that keep the tank stable.

## Key Features
- Live tank condition monitoring
- Scheduled fish feeding
- Cleaning or water circulation control
- Threshold-based alerts
- Optional remote monitoring from a phone or dashboard

## Hardware Requirements
- ESP32 development board
- Water level sensor
- Temperature sensor
- Optional pH or turbidity sensor
- Servo or stepper motor for feeding
- Relay or pump for cleaning or filtration
- OLED/LCD display and buzzer

## Software Requirements
- Arduino IDE or PlatformIO
- MQTT, Blynk, or a web dashboard for status updates
- Basic scheduling logic for automated actions

## How To Run This Project
Follow these steps in order if you want a simple setup path.

### Step-by-Step Setup
1. Install Arduino IDE.
2. Open Arduino IDE and add ESP32 support from Boards Manager.
3. Install the `ESP32Servo` library from the Library Manager.
4. Open the file named [main.ino](main.ino).
5. Check the sensor pins, servo pin, relay pin, and buzzer pin so they match your wiring.
6. Make sure the feeder servo has its own safe power supply if needed.
7. Connect the ESP32 to your computer by USB.
8. Select the correct ESP32 board and COM port.
9. Click Upload.
10. Open Serial Monitor and watch the tank readings.

### Command-Line Method
Use these commands from the project folder after installing `arduino-cli`:

```bash
arduino-cli core update-index
arduino-cli core install esp32:esp32
arduino-cli lib install "ESP32Servo"
arduino-cli compile --fqbn esp32:esp32:esp32 "d:/Puthusus/IOT Projects/automated-fish-tank-monitoring-cleaning-feeding-system-esp32"
arduino-cli upload -p COM3 --fqbn esp32:esp32:esp32 "d:/Puthusus/IOT Projects/automated-fish-tank-monitoring-cleaning-feeding-system-esp32"
```

Replace `COM3` with the port name shown on your computer.

### What You Should See
- Water level and temperature values in Serial Monitor.
- The feeder runs at the scheduled time.
- The pump relay turns on during the cleaning cycle.
- Alerts appear when the water is too low or too high.

## How It Works
1. Sensors capture water level and environmental data.
2. The ESP32 checks the readings against safe thresholds.
3. A feeder motor dispenses food on schedule.
4. Pumps or relays can run cleaning or filtration cycles.
5. Alerts appear if the tank needs attention.

## Roadmap & Block Diagram
![Automated Fish Tank Monitoring roadmap and block diagram](roadmap.svg)

## Possible Enhancements
- Automatic water replacement
- Camera-based fish activity detection
- Historical tank data logging
- Manual override controls in a mobile app
- Smarter scheduling based on sensor trends

## GitHub Profile Summary
This is a practical home-automation project that combines sensing, automation, and scheduled control for easier aquarium maintenance.
