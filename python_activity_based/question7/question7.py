# Multi-Plan Telecommunications Cost Optimization

def calculate_excess(plan, usage):
    """Extra charge for data and call minutes used beyond the plan's limits."""
    name, price, validity, data_gb, minutes, per_gb, per_min = plan
    extra_data = max(0, usage["data_gb"] - data_gb)
    extra_minutes = max(0, usage["minutes"] - minutes)
    return extra_data * per_gb + extra_minutes * per_min


def check_eligibility(plan, usage, budget):
    """Return (eligible, total_cost, reason)."""
    name, price, validity, data_gb, minutes, per_gb, per_min = plan
    excess = calculate_excess(plan, usage)
    total = price + excess
    if validity < usage["days"]:
        return False, total, "validity too short"
    if total > budget:
        return False, total, "over budget"
    return True, total, "eligible"


def evaluate_plans(plans, usage, budget):
    """Evaluate every plan and return a list of result dictionaries."""
    results = []
    for plan in plans:
        eligible, total, reason = check_eligibility(plan, usage, budget)
        results.append({
            "name": plan[0],
            "price": plan[1],
            "excess": calculate_excess(plan, usage),
            "total": total,
            "eligible": eligible,
            "reason": reason,
        })
    return results


def best_plan(results):
    """Cheapest eligible plan (ties: lower base price). None if nothing fits."""
    eligible = [r for r in results if r["eligible"]]
    if not eligible:
        return None
    return min(eligible, key=lambda r: (r["total"], r["price"]))


if __name__ == "__main__":
    plans = [
        ("Basic",   199,  28,  28, 100, 10, 1.0),
        ("Value",   299,  28,  56, 300,  8, 0.8),
        ("Max",     499,  56, 112, 600,  5, 0.5),
        ("Monthly", 399,  30,  45, 200,  6, 0.6),
        ("Short",   149,  14,  14,  50, 12, 1.2),
    ]
    usage = {"data_gb": 40, "minutes": 150, "days": 28}
    budget = 450

    results = evaluate_plans(plans, usage, budget)
    print(f"{'Plan':<9}{'Price':>6}{'Excess':>8}{'Total':>8}  Status")
    for r in results:
        print(f"{r['name']:<9}{r['price']:>6}{r['excess']:>8.1f}{r['total']:>8.1f}  {r['reason']}")
    best = best_plan(results)
    if best:
        print(f"\nBest plan: {best['name']} (total Rs {best['total']:.1f})")
    else:
        print("\nNo plan fits the budget and validity.")