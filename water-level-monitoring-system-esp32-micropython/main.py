import random
import time

try:
    from machine import Pin, time_pulse_us
    HARDWARE_MODE = True
except ImportError:
    HARDWARE_MODE = False

    class Pin:
        OUT = 1
        IN = 0

        def __init__(self, pin_number, mode):
            self.pin_number = pin_number
            self.mode = mode
            self._value = 0

        def value(self, new_value=None):
            if new_value is None:
                return self._value
            self._value = int(bool(new_value))

    def time_pulse_us(pin, state, timeout):
        simulated_distance_cm = random.choice([6, 12, 20, 30, 35])
        return int((simulated_distance_cm * 2) / 0.0343)


trigger = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)
red_led = Pin(26, Pin.OUT)
green_led = Pin(27, Pin.OUT)
buzzer = Pin(25, Pin.OUT)
relay = Pin(33, Pin.OUT)

LOW_LEVEL_CM = 25
HIGH_LEVEL_CM = 8

def measure_distance_cm():
    if not HARDWARE_MODE:
        pulse = time_pulse_us(echo, 1, 30000)
        return (pulse * 0.0343) / 2

    trigger.value(0)
    time.sleep_us(2)
    trigger.value(1)
    time.sleep_us(10)
    trigger.value(0)

    pulse = time_pulse_us(echo, 1, 30000)
    if pulse < 0:
        return None

    return (pulse * 0.0343) / 2

def set_state(distance):
    if distance is None:
        red_led.value(1)
        green_led.value(0)
        buzzer.value(1)
        relay.value(0)
        print("Sensor timeout")
        return

    print("Distance: {:.2f} cm".format(distance))

    if distance >= LOW_LEVEL_CM:
        red_led.value(1)
        green_led.value(0)
        buzzer.value(1)
        relay.value(1)
        print("Water level low")
    elif distance <= HIGH_LEVEL_CM:
        red_led.value(1)
        green_led.value(0)
        buzzer.value(1)
        relay.value(0)
        print("Water level high")
    else:
        red_led.value(0)
        green_led.value(1)
        buzzer.value(0)
        relay.value(0)
        print("Water level normal")

def main():
    if not HARDWARE_MODE:
        print("Running in desktop simulation mode. Install MicroPython firmware on ESP32 for real hardware output.")

    while True:
        distance = measure_distance_cm()
        set_state(distance)
        time.sleep(2)

main()