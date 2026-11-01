# Smart Public Transport Fare Reconciliation

BASE_FARES = {"R1": 20, "R2": 35, "R3": 50}            
DISCOUNTS = {"Adult": 1.0, "Student": 0.5, "Senior": 0.6, "Child": 0.0}  
TOLERANCE = 1  

def calculate_fare(route, category):
    """Fare for ONE passenger. Returns None if route or category is unknown."""
    if route not in BASE_FARES or category not in DISCOUNTS:
        return None
    return BASE_FARES[route] * DISCOUNTS[category]

def calculate_expected_revenue(tickets):
    """Return (expected_by_route, invalid_tickets)."""
    expected = {route: 0 for route in BASE_FARES}
    invalid = []
    for route, category, count in tickets:
        fare = calculate_fare(route, category)
        if fare is None or count < 0:
            invalid.append((route, category, count))
        else:
            expected[route] += fare * count
    return expected, invalid

def reconcile(expected, collected, tolerance=TOLERANCE):
    """Compare expected and collected revenue for every route."""
    report = []
    for route in expected:
        exp = expected[route]
        col = collected.get(route, 0)
        diff = col - exp
        if abs(diff) <= tolerance:
            status = "MATCH"
        elif diff < 0:
            status = "SHORTAGE"
        else:
            status = "EXCESS"
        report.append((route, exp, col, diff, status))
    return report

if __name__ == "__main__":
    tickets = [
        ("R1", "Adult", 10), ("R1", "Student", 6), ("R1", "Child", 3),
        ("R2", "Adult", 8),  ("R2", "Senior", 4),
        ("R3", "Adult", 5),  ("R3", "Student", 2),
        ("R9", "Adult", 2),                 
        ("R2", "Tourist", 1),               
    ]
    collected = {"R1": 260, "R2": 400, "R3": 310}

    expected, invalid = calculate_expected_revenue(tickets)
    report = reconcile(expected, collected)

    print(f"{'Route':<7}{'Expected':>10}{'Collected':>11}{'Diff':>8}  Status")
    for route, exp, col, diff, status in report:
        print(f"{route:<7}{exp:>10.1f}{col:>11.1f}{diff:>8.1f}  {status}")
    print("\nTotal expected :", sum(r[1] for r in report))
    print("Total collected:", sum(r[2] for r in report))
    print("Net difference :", sum(r[3] for r in report))
    print("Invalid tickets:", invalid)
    