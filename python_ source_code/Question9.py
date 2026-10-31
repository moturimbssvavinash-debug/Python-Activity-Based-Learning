# Hospital Billing and Patient Classification

SENIOR_AGE = 60
SENIOR_DISCOUNT = 10        
LOW_INCOME_DISCOUNT = 20    
HIGH_BILL_LIMIT = 20000     
HIGH_BILL_DISCOUNT = 5      
MAX_CONCESSION = 5000       

PAYMENT_POLICY = [
    (2000, "Category A", "Pay in full at counter"),
    (10000, "Category B", "Pay in full or 2 installments"),
    (float("inf"), "Category C", "50% advance deposit + installment plan"),
]

def validate_patient(patient):
    """Return a list of billing/data errors (empty list means valid)."""
    errors = []
    if len(patient) != 7:
        return ["Wrong number of fields"]
    pid, name, age, low_income, consult, diag, treat = patient
    if not isinstance(name, str) or name.strip() == "":
        errors.append("Name is missing")
    if not isinstance(age, int) or age < 0 or age > 120:
        errors.append("Age must be between 0 and 120")
    for label, charge in [("Consultation", consult), ("Diagnostic", diag), ("Treatment", treat)]:
        if not isinstance(charge, (int, float)) or charge < 0:
            errors.append(f"{label} charge must be a non-negative number")
    if not errors and consult + diag + treat == 0:
        errors.append("Total bill is zero")
    return errors

def calculate_subtotal(patient):
    return patient[4] + patient[5] + patient[6]

def find_concession_percent(patient, subtotal):
    """Concessions do NOT stack: the highest applicable percentage is used."""
    age, low_income = patient[2], patient[3]
    options = []
    if age >= SENIOR_AGE:
        options.append(SENIOR_DISCOUNT)
    if low_income:
        options.append(LOW_INCOME_DISCOUNT)
    if subtotal > HIGH_BILL_LIMIT:
        options.append(HIGH_BILL_DISCOUNT)
    return max(options) if options else 0

def classify_patient(net_amount):
    """Return (category, payment_rule) from the payment policy."""
    for limit, category, rule in PAYMENT_POLICY:
        if net_amount <= limit:
            return category, rule

def process_bill(patient):
    """Validate, calculate and classify. Returns a dictionary."""
    errors = validate_patient(patient)
    if errors:
        return {"id": patient[0], "valid": False, "errors": errors}
    subtotal = calculate_subtotal(patient)
    percent = find_concession_percent(patient, subtotal)
    concession = min(subtotal * percent / 100, MAX_CONCESSION)
    net = round(subtotal - concession, 2)
    category, rule = classify_patient(net)
    return {"id": patient[0], "name": patient[1], "valid": True,
            "subtotal": subtotal, "percent": percent,
            "concession": round(concession, 2), "net": net,
            "category": category, "rule": rule}

if __name__ == "__main__":
    patients = [
        ("P01", "Ravi",   35, False,  500,  800,  400),
        ("P02", "Lakshmi", 68, False,  600, 2500, 4000),
        ("P03", "Suresh", 45, True,   500, 3000, 12000),
        ("P04", "Anil",   50, False, 1000, 8000, 30000),
        ("P05", "",       30, False,  500,  200,   100),
        ("P06", "Meena",  25, False,  500,  -300,  100),
    ]
    for p in patients:
        r = process_bill(p)
        print("Patient", r["id"], end=": ")
        if not r["valid"]:
            print("INVALID ->", "; ".join(r["errors"]))
            continue
        print(r["name"])
        print(f"  Subtotal : Rs {r['subtotal']}")
        print(f"  Concession: {r['percent']}% = Rs {r['concession']}")
        print(f"  Net bill : Rs {r['net']}")
        print(f"  Class    : {r['category']} - {r['rule']}")
        