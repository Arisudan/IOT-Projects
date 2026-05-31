from __future__ import annotations

import argparse
import csv
from pathlib import Path

DEFAULT_DATA_FILE = Path("sensor_data.csv")

SAMPLE_ROWS = [
    (72.0, 1.3, 58.0, 0.9),
    (74.0, 1.8, 60.0, 1.1),
    (78.5, 2.4, 64.0, 1.4),
    (81.0, 2.9, 68.0, 1.6),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Industrial Equipment Failure Prediction using Sensor Data")
    parser.add_argument("--data-file", default=str(DEFAULT_DATA_FILE), help="CSV file with temperature,vibration,current,load columns")
    return parser.parse_args()


def load_rows(data_file: Path) -> list[tuple[float, float, float, float]]:
    if data_file.exists():
        rows: list[tuple[float, float, float, float]] = []
        with data_file.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                try:
                    rows.append(
                        (
                            float(row["temperature"]),
                            float(row["vibration"]),
                            float(row["current"]),
                            float(row["load"]),
                        )
                    )
                except (KeyError, TypeError, ValueError):
                    continue
        if rows:
            return rows
    return SAMPLE_ROWS


def risk_score(row: tuple[float, float, float, float]) -> tuple[int, str]:
    temperature, vibration, current, load = row
    score = 0
    score += max(0, int((temperature - 65) * 2))
    score += max(0, int(vibration * 10))
    score += max(0, int((current - 55) * 1.2))
    score += max(0, int((load - 70) * 1.5))
    score = max(0, min(100, score))

    if score < 30:
        label = "Low Risk"
    elif score < 60:
        label = "Medium Risk"
    else:
        label = "High Risk"

    return score, label


def main() -> None:
    args = parse_args()
    data_file = Path(args.data_file)
    rows = load_rows(data_file)

    print("Industrial Equipment Failure Prediction using Sensor Data")
    print("-------------------------------------------------------")
    print(f"Data source: {data_file}")

    for index, row in enumerate(rows, start=1):
        score, label = risk_score(row)
        temperature, vibration, current, load = row
        print(f"Sample {index}")
        print(f"  Temperature: {temperature:.1f}")
        print(f"  Vibration  : {vibration:.1f}")
        print(f"  Current    : {current:.1f}")
        print(f"  Load       : {load:.1f}")
        print(f"  Risk Score : {score}/100")
        print(f"  Status     : {label}")


if __name__ == "__main__":
    main()
