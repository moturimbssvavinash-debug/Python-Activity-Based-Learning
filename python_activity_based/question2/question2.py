# Railway Fare and Reservation Calculator


SLABS = [(100, 1.00), (300, 0.80), (float("inf"), 0.60)]

CLASSES = {
    "SL": (1.0, 20, 120),   
    "3A": (2.2, 40, 180),   
    "2A": (3.0, 50, 200),   
    "1A": (4.5, 60, 240),  
}

MIN_FARE = 30   


def base_fare(distance):
    """Slab-wise fare for a Sleeper-class full ticket."""
    fare, previous_limit = 0.0, 0
    for limit, rate in SLABS:
        if distance > previous_limit:
            km_in_slab = min(distance, limit) - previous_limit
            fare += km_in_slab * rate
        previous_limit = limit
    return max(fare, MIN_FARE)


def concession_percent(age, gender):
    """Return (concession %, category name)."""
    if age < 5:
        return 100, "Infant (free)"
    if age <= 11:
        return 50, "Child"
    if gender == "F" and age >= 58:
        return 50, "Senior Woman"
    if gender == "M" and age >= 60:
        return 40, "Senior Man"
    return 0, "Adult"


def passenger_fare(passenger, travel_class, distance):
    """Fare details for ONE passenger."""
    multiplier, res_fee, _ = CLASSES[travel_class]
    class_fare = base_fare(distance) * multiplier
    percent, category = concession_percent(passenger["age"], passenger["gender"])
    discount = class_fare * percent / 100
    fare_after = class_fare - discount
    reservation = 0 if percent == 100 else res_fee      
    return {
        "name": passenger["name"], "age": passenger["age"], "category": category,
        "class_fare": round(class_fare, 2), "discount": round(discount, 2),
        "fare": round(fare_after, 2), "reservation": reservation,
        "total": round(fare_after + reservation, 2),
    }


def calculate_booking(passengers, travel_class, distance):
    details = [passenger_fare(p, travel_class, distance) for p in passengers]
    return {"class": travel_class, "distance": distance, "details": details,
            "grand_total": round(sum(d["total"] for d in details), 2)}


def cancellation_penalty(detail, travel_class, hours_before):
    """Penalty for one passenger. Reservation fee is never refunded."""
    if detail["total"] == 0:
        return 0.0
    clerkage = CLASSES[travel_class][2]
    if hours_before >= 48:
        penalty = min(clerkage, detail["fare"])          
    elif hours_before >= 12:
        penalty = detail["fare"] * 0.25                  
    elif hours_before >= 4:
        penalty = detail["fare"] * 0.50                  
    else:
        penalty = detail["fare"]                         
    return round(penalty, 2)


def cancel_booking(booking, hours_before):
    rows, total_refund = [], 0.0
    for d in booking["details"]:
        penalty = cancellation_penalty(d, booking["class"], hours_before)
        refund = max(d["fare"] - penalty, 0)             
        rows.append((d["name"], d["total"], penalty, d["reservation"], round(refund, 2)))
        total_refund += refund
    return rows, round(total_refund, 2)


def print_booking(booking):
    print(f"Class: {booking['class']}   Distance: {booking['distance']} km   "
          f"Base fare (Sleeper): Rs {base_fare(booking['distance']):.2f}")
    print("-" * 78)
    print(f"{'Name':<9}{'Age':<5}{'Category':<15}{'ClassFare':<11}{'Discount':<10}{'Fare':<9}{'ResFee':<8}{'Total'}")
    print("-" * 78)
    for d in booking["details"]:
        print(f"{d['name']:<9}{d['age']:<5}{d['category']:<15}{d['class_fare']:<11.2f}"
              f"{d['discount']:<10.2f}{d['fare']:<9.2f}{d['reservation']:<8}{d['total']:.2f}")
    print("-" * 78)
    print(f"GRAND TOTAL = Rs {booking['grand_total']:.2f}")


def print_cancellation(booking, hours):
    rows, refund = cancel_booking(booking, hours)
    print(f"\nCancellation {hours} hours before departure")
    print("-" * 66)
    print(f"{'Name':<9}{'Paid':<10}{'Penalty':<10}{'ResFee(no refund)':<19}{'Refund'}")
    for name, paid, penalty, res, ref in rows:
        print(f"{name:<9}{paid:<10.2f}{penalty:<10.2f}{res:<19}{ref:.2f}")
    print(f"TOTAL REFUND = Rs {refund:.2f}")


if __name__ == "__main__":
    family = [
        {"name": "Ravi",   "age": 35, "gender": "M"},
        {"name": "Sita",   "age": 32, "gender": "F"},
        {"name": "Kiran",  "age": 8,  "gender": "M"},
        {"name": "Baby",   "age": 2,  "gender": "F"},
        {"name": "Grandpa","age": 65, "gender": "M"},
        {"name": "Granny", "age": 60, "gender": "F"},
    ]
    print("=" * 78)
    print("RAILWAY FARE CALCULATOR - Booking 1")
    print("=" * 78)
    booking = calculate_booking(family, "3A", 450)
    print_booking(booking)
    for h in (72, 24, 6, 2):
        print_cancellation(booking, h)

    print("\n" + "=" * 78)
    print("Booking 2: single adult, short trip (minimum fare check)")
    print("=" * 78)
    print_booking(calculate_booking([{"name": "Amit", "age": 25, "gender": "M"}], "SL", 20))