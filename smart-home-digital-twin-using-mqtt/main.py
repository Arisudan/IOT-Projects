import argparse
import json
import random
import time

DEFAULT_BROKER = "broker.hivemq.com"
DEFAULT_TOPIC = "home/digital_twin/state"
DEFAULT_INTERVAL = 5

state = {
    "living_room_light": "OFF",
    "fan": "OFF",
    "temperature": 24.0,
    "door": "CLOSED",
}

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None


def print_dashboard(broker: str, topic: str) -> None:
    print("\n=== Smart Home Digital Twin ===")
    print(f"MQTT broker : {broker}")
    print(f"MQTT topic  : {topic}")
    for key, value in state.items():
        print(f"{key:18s}: {value}")


def update_from_payload(payload: str) -> None:
    try:
        data = json.loads(payload)
    except json.JSONDecodeError:
        return

    for key in state:
        if key in data:
            state[key] = data[key]


def simulate_environment() -> None:
    state["temperature"] = round(22 + random.random() * 6, 1)
    state["living_room_light"] = random.choice(["ON", "OFF"])
    state["fan"] = random.choice(["ON", "OFF"])
    state["door"] = random.choice(["OPEN", "CLOSED"])


def run_simulation(broker: str, topic: str, interval: int) -> None:
    print("paho-mqtt is not installed, so the project is running in simulation mode.")
    print("Install it later with: pip install paho-mqtt")
    while True:
        simulate_environment()
        print_dashboard(broker, topic)
        time.sleep(interval)


def run_mqtt_client(broker: str, topic: str, interval: int) -> None:
    def on_connect(client, userdata, flags, rc):
        print(f"Connected to MQTT broker with result code {rc}")
        client.subscribe(topic)

    def on_message(client, userdata, msg):
        update_from_payload(msg.payload.decode("utf-8"))
        print_dashboard()

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(broker, 1883, 60)
    client.loop_start()

    print("Listening for MQTT updates. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(interval)
    except KeyboardInterrupt:
        client.loop_stop()
        client.disconnect()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smart Home Digital Twin using MQTT")
    parser.add_argument("--broker", default=DEFAULT_BROKER, help="MQTT broker host")
    parser.add_argument("--topic", default=DEFAULT_TOPIC, help="MQTT topic to subscribe to")
    parser.add_argument("--interval", type=int, default=DEFAULT_INTERVAL, help="Refresh interval in seconds")
    parser.add_argument("--simulate", action="store_true", help="Force simulation mode even if MQTT is available")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print_dashboard(args.broker, args.topic)
    if mqtt is None or args.simulate:
        run_simulation(args.broker, args.topic, args.interval)

    try:
        run_mqtt_client(args.broker, args.topic, args.interval)
    except Exception as error:
        print(f"MQTT mode failed ({error}). Switching to simulation mode.")
        run_simulation(args.broker, args.topic, args.interval)


if __name__ == "__main__":
    main()
