# Intelligent Room Occupancy Detection System

![ESP32](https://img.shields.io/badge/Board-ESP32-blue)
![IoT](https://img.shields.io/badge/Domain-IoT-green)
![Status](https://img.shields.io/badge/Status-Documentation%20Ready-brightgreen)

## Overview
This project detects whether a room is occupied or empty by using a motion sensor with an ESP32. It can be used for smart buildings, offices, meeting rooms, and home automation.

## At a Glance
- Sensor: PIR motion sensor
- Output: LED, buzzer, and web status page
- File to run: [main.ino](main.ino)

## What You Need
- ESP32 board
- PIR motion sensor
- LED and resistor
- Buzzer
- Wi-Fi network

## How To Run This Project
This project is simple to set up with Arduino IDE.

### Step-by-Step Setup
1. Install Arduino IDE.
2. Install ESP32 support from Boards Manager.
3. Open [main.ino](main.ino).
4. Connect the PIR sensor, LED, and buzzer as shown in your wiring plan.
5. Update the Wi-Fi name and password in the sketch.
6. Upload the sketch to the ESP32.
7. Open Serial Monitor to see the occupancy status.
8. Open the IP address shown in the monitor to see the web page.

### Commands To Run
```bash
arduino-cli core update-index
arduino-cli core install esp32:esp32
arduino-cli compile --fqbn esp32:esp32:esp32 "d:/Puthusus/IOT Projects/intelligent-room-occupancy-detection-system"
arduino-cli upload -p COM3 --fqbn esp32:esp32:esp32 "d:/Puthusus/IOT Projects/intelligent-room-occupancy-detection-system"
```

## What You Should See
- LED turns on when motion is detected
- Web page shows occupied or empty
- Serial Monitor prints room status

## Roadmap & Block Diagram
![Intelligent Room Occupancy roadmap and block diagram](roadmap.svg)

## Possible Enhancements
- Room booking dashboard
- Occupancy history logging
- Mobile notifications when a room becomes free
- Integration with smart lighting and HVAC

## GitHub Profile Summary
A practical occupancy detection project that uses ESP32 sensing and live status reporting.
