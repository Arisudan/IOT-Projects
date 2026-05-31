from __future__ import annotations

import argparse
import csv
import random
from dataclasses import dataclass
from pathlib import Path

DEFAULT_DATA_FILE = Path("motor_data.csv")


@dataclass
class MotorReading:
    vibration: float
    temperature: float
    current: float
    runtime_hours: float


DEFAULT_READING = MotorReading(vibration=2.4, temperature=58.0, current=11.2, runtime_hours=420.0)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Predictive Maintenance System for Industrial Motors")
    parser.add_argument("--data-file", default=str(DEFAULT_DATA_FILE), help="Optional CSV with vibration,temperature,current,runtime_hours columns")
    return parser.parse_args()


def load_reading(data_file: Path) -> MotorReading:
    if data_file.exists():
        with data_file.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            first_row = next(reader, None)
            if first_row:
                try:
                    return MotorReading(
                        vibration=float(first_row.get("vibration", DEFAULT_READING.vibration)),
                        temperature=float(first_row.get("temperature", DEFAULT_READING.temperature)),
                        current=float(first_row.get("current", DEFAULT_READING.current)),
                        runtime_hours=float(first_row.get("runtime_hours", DEFAULT_READING.runtime_hours)),
                    )
                except (TypeError, ValueError):
                    pass

    return MotorReading(
        vibration=round(DEFAULT_READING.vibration + random.uniform(-0.5, 1.2), 2),
        temperature=round(DEFAULT_READING.temperature + random.uniform(-3, 12), 2),
        current=round(DEFAULT_READING.current + random.uniform(-1.0, 2.5), 2),
        runtime_hours=DEFAULT_READING.runtime_hours,
    )


def compute_health(reading: MotorReading) -> tuple[int, str]:
    score = 100
    score -= max(0, int((reading.vibration - 2.0) * 12))
    score -= max(0, int((reading.temperature - 55.0) * 2))
    score -= max(0, int((reading.current - 10.5) * 8))
    score -= max(0, int(reading.runtime_hours / 200))
    score = max(0, min(100, score))

    if score >= 80:
        advice = "Motor health looks normal."
    elif score >= 60:
        advice = "Monitor the motor and plan maintenance soon."
    else:
        advice = "Service the motor soon to reduce failure risk."

    return score, advice


def main() -> None:
    args = parse_args()
    data_file = Path(args.data_file)
    reading = load_reading(data_file)
    score, advice = compute_health(reading)

    print("Predictive Maintenance System for Industrial Motors")
    print("---------------------------------------------------")
    print(f"Data source: {data_file}")
    print(f"Vibration      : {reading.vibration:.2f}")
    print(f"Temperature    : {reading.temperature:.2f} C")
    print(f"Current        : {reading.current:.2f} A")
    print(f"Runtime Hours  : {reading.runtime_hours:.0f}")
    print(f"Health Score   : {score}/100")
    print(f"Recommendation : {advice}")


if __name__ == "__main__":
    main()
