# Warehouse Inventory Reconciliation


TOLERANCE = 0   

def validate_record(rec):
    """Return a list of errors (empty list = valid)."""
    if len(rec) != 7:
        return ["Wrong number of fields"]
    name, opening, incoming, dispatched, closing, reorder, max_level = rec
    errors = []
    for label, value in [("Opening", opening), ("Incoming", incoming),
                         ("Dispatched", dispatched), ("Closing", closing),
                         ("Reorder level", reorder), ("Max level", max_level)]:
        if not isinstance(value, int) or value < 0:
            errors.append(f"{label} must be a whole number >= 0")
    if not errors:
        if dispatched > opening + incoming:
            errors.append("Dispatched is more than available stock")
        if max_level < reorder:
            errors.append("Max level is less than reorder level")
    return errors


def expected_closing(opening, incoming, dispatched):
    return opening + incoming - dispatched


def find_discrepancy(expected, actual, tolerance=TOLERANCE):
    """Return (difference, status). Difference = actual - expected."""
    diff = actual - expected
    if abs(diff) <= tolerance:
        return diff, "OK"
    if diff < 0:
        return diff, "SHORTAGE"
    return diff, "SURPLUS"


def replenishment_needed(actual, reorder_level, max_level):
    """If stock is below the reorder level, order enough to reach max level."""
    if actual < reorder_level:
        return max_level - actual
    return 0


def reconcile_product(rec):
    errors = validate_record(rec)
    if errors:
        return {"product": rec[0], "valid": False, "errors": errors}
    name, opening, incoming, dispatched, closing, reorder, max_level = rec
    exp = expected_closing(opening, incoming, dispatched)
    diff, status = find_discrepancy(exp, closing)
    order = replenishment_needed(closing, reorder, max_level)
    return {"product": name, "valid": True, "expected": exp, "actual": closing,
            "diff": diff, "status": status, "reorder": order}


if __name__ == "__main__":
    records = [
        ("Rice",   500, 200, 450, 250, 150, 600),
        ("Oil",    300, 100, 350,  40, 100, 400),
        ("Sugar",  200,  50, 100, 160, 100, 300),
        ("Salt",   100,  20, 150,  10,  30, 200),
        ("Tea",     80,  40,  60,  -5,  20, 100),
    ]
    print(f"{'Product':<8}{'Expected':>9}{'Actual':>8}{'Diff':>6}  {'Status':<9}{'Order Qty':>9}")
    invalid = []
    for rec in records:
        r = reconcile_product(rec)
        if not r["valid"]:
            invalid.append(r)
            continue
        print(f"{r['product']:<8}{r['expected']:>9}{r['actual']:>8}{r['diff']:>6}  {r['status']:<9}{r['reorder']:>9}")
    print()
    for r in invalid:
        print("INVALID record:", r["product"], "->", "; ".join(r["errors"]))