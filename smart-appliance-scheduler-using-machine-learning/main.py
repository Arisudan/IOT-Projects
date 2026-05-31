from __future__ import annotations

import argparse
import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

@dataclass
class UsageRecord:
    appliance: str
    hour: int
    day: str


SAMPLE_HISTORY = [
    UsageRecord("Washing Machine", 9, "Mon"),
    UsageRecord("Washing Machine", 10, "Wed"),
    UsageRecord("Washing Machine", 9, "Fri"),
    UsageRecord("Water Heater", 6, "Mon"),
    UsageRecord("Water Heater", 6, "Tue"),
    UsageRecord("Water Heater", 7, "Wed"),
    UsageRecord("Air Conditioner", 18, "Mon"),
    UsageRecord("Air Conditioner", 19, "Tue"),
    UsageRecord("Air Conditioner", 18, "Wed"),
]

DEFAULT_HISTORY_FILE = Path("usage_history.csv")


def load_history(history_file: Path) -> list[UsageRecord]:
    if not history_file.exists():
        return SAMPLE_HISTORY

    records: list[UsageRecord] = []
    with history_file.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            try:
                appliance = row["appliance"]
                hour = int(row["hour"])
                day = row.get("day", "Unknown")
            except (KeyError, TypeError, ValueError):
                continue
            records.append(UsageRecord(appliance, hour, day))

    return records or SAMPLE_HISTORY


def predict_best_hour(records: list[UsageRecord]) -> dict[str, int]:
    grouped: dict[str, list[int]] = defaultdict(list)
    for record in records:
        grouped[record.appliance].append(record.hour)

    predictions: dict[str, int] = {}
    for appliance, hours in grouped.items():
        most_common_hour, _ = Counter(hours).most_common(1)[0]
        predictions[appliance] = most_common_hour
    return predictions


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smart Appliance Scheduler using Machine Learning")
    parser.add_argument("--history-file", default=str(DEFAULT_HISTORY_FILE), help="CSV file with appliance,hour,day columns")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    history = load_history(Path(args.history_file))
    print("Smart Appliance Scheduler using Machine Learning")
    print("------------------------------------------------")
    print(f"Data source: {args.history_file}")
    predictions = predict_best_hour(history)

    for appliance, hour in predictions.items():
        print(f"{appliance}: suggested run hour -> {hour:02d}:00")

    print("\nThis is a starter model based on the most common usage hour.")


if __name__ == "__main__":
    main()
