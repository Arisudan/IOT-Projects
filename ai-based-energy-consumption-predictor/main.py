from __future__ import annotations

import argparse
import csv
import math
from pathlib import Path

DEFAULT_DATA_FILE = Path("energy_data.csv")
DEFAULT_DAYS_AHEAD = 3


def load_samples(data_file: Path) -> list[tuple[float, float]]:
    if data_file.exists():
        samples: list[tuple[float, float]] = []
        with data_file.open(newline="", encoding="utf-8") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                try:
                    day = float(row["day"])
                    kwh = float(row["kwh"])
                except (KeyError, TypeError, ValueError):
                    continue
                samples.append((day, kwh))
        if samples:
            return samples

    return [
        (1, 18.2),
        (2, 19.0),
        (3, 20.1),
        (4, 21.0),
        (5, 21.8),
        (6, 22.3),
        (7, 23.1),
        (8, 23.8),
    ]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="AI-Based Energy Consumption Predictor")
    parser.add_argument("--data-file", default=str(DEFAULT_DATA_FILE), help="CSV file with day and kwh columns")
    parser.add_argument("--days-ahead", type=int, default=DEFAULT_DAYS_AHEAD, help="How many future days to predict")
    return parser.parse_args()


def fit_line(samples: list[tuple[float, float]]) -> tuple[float, float]:
    n = len(samples)
    sum_x = sum(x for x, _ in samples)
    sum_y = sum(y for _, y in samples)
    sum_x2 = sum(x * x for x, _ in samples)
    sum_xy = sum(x * y for x, y in samples)

    denominator = n * sum_x2 - sum_x * sum_x
    if math.isclose(denominator, 0.0):
        return 0.0, sum_y / n

    slope = (n * sum_xy - sum_x * sum_y) / denominator
    intercept = (sum_y - slope * sum_x) / n
    return slope, intercept


def predict_next(samples: list[tuple[float, float]], days_ahead: int = 3) -> list[tuple[int, float]]:
    slope, intercept = fit_line(samples)
    last_day = int(max(day for day, _ in samples))
    predictions: list[tuple[int, float]] = []

    for offset in range(1, days_ahead + 1):
        day = last_day + offset
        value = slope * day + intercept
        predictions.append((day, round(value, 2)))

    return predictions


def main() -> None:
    args = parse_args()
    samples = load_samples(Path(args.data_file))
    print("AI-Based Energy Consumption Predictor")
    print("------------------------------------")
    print(f"Data source: {args.data_file}")
    print("Loaded samples:")
    for day, kwh in samples:
        print(f"Day {int(day):02d}: {kwh:.2f} kWh")

    print("\nPredicted energy use:")
    for day, value in predict_next(samples, days_ahead=args.days_ahead):
        print(f"Day {day:02d}: {value:.2f} kWh")


if __name__ == "__main__":
    main()
