# Environmental Monitoring Data Analyzer
# Data: nested list -> [station_name, [reading1, reading2, ...]]

# Thresholds: (upper_limit, label). A reading <= limit gets that label.
THRESHOLDS = [
    (50, "Good"),
    (100, "Moderate"),
    (150, "Unhealthy"),
    (float("inf"), "Hazardous"),
]


def clean_readings(readings):
    """Keep only valid numbers (not text, not negative)."""
    valid = []
    for r in readings:
        if isinstance(r, (int, float)) and r >= 0:
            valid.append(r)
    return valid


def calculate_average(values):
    """Average of a list; returns None for an empty list."""
    if len(values) == 0:
        return None
    return sum(values) / len(values)


def find_extremes(values):
    """Return (minimum, maximum); (None, None) for an empty list."""
    if len(values) == 0:
        return None, None
    return min(values), max(values)


def classify(value, thresholds):
    """Return the category label for one reading."""
    for limit, label in thresholds:
        if value <= limit:
            return label
    return "Unknown"


def analyze_station(name, readings, thresholds):
    """Analyse one station and return a dictionary of results."""
    valid = clean_readings(readings)
    low, high = find_extremes(valid)
    avg = calculate_average(valid)
    result = {
        "station": name,
        "count": len(valid),
        "skipped": len(readings) - len(valid),
        "average": avg,
        "min": low,
        "max": high,
        "avg_class": classify(avg, thresholds) if avg is not None else "No data",
        "labels": [classify(v, thresholds) for v in valid],
    }
    return result


def analyze_all(data, thresholds):
    return [analyze_station(name, readings, thresholds) for name, readings in data]


if __name__ == "__main__":
    data = [
        ["Station A", [35, 42, 58, 47]],
        ["Station B", [90, 120, 160, 75]],
        ["Station C", [20, "error", -5, 30]],
        ["Station D", []],
    ]
    for r in analyze_all(data, THRESHOLDS):
        print("Station:", r["station"])
        if r["count"] == 0:
            print("  No valid readings")
            continue
        print(f"  Valid readings: {r['count']} (skipped {r['skipped']})")
        print(f"  Average: {r['average']:.2f} -> {r['avg_class']}")
        print(f"  Min: {r['min']}  Max: {r['max']}")
        print("  Categories:", r["labels"])