# University Scholarship Allocation System

MIN_AGGREGATE = 60.0      
MIN_SUBJECT   = 40        
MIN_ATTENDANCE = 75.0     
MAX_INCOME    = 300000   
TOTAL_SEATS   = 3         
TIE_SUBJECT   = "Maths"   


def calculate_aggregate(marks):
    """Average of all subject marks (each out of 100)."""
    return sum(marks.values()) / len(marks)


def check_eligibility(student):
    """Return (True, '') if eligible, else (False, reason)."""
    agg = calculate_aggregate(student["marks"])
    if agg < MIN_AGGREGATE:
        return False, f"Aggregate {agg:.2f}% < {MIN_AGGREGATE}%"
    for subject, mark in student["marks"].items():
        if mark < MIN_SUBJECT:
            return False, f"{subject} mark {mark} < {MIN_SUBJECT}"
    if student["attendance"] < MIN_ATTENDANCE:
        return False, f"Attendance {student['attendance']}% < {MIN_ATTENDANCE}%"
    if student["income"] > MAX_INCOME:
        return False, f"Income {student['income']} > {MAX_INCOME}"
    return True, ""


def ranking_key(student):
    """
    Sort key. Python sorts smallest first, so we negate
    values where a HIGHER number is better.
    Tie-break order:
      1. Higher aggregate
      2. Higher marks in TIE_SUBJECT
      3. Lower family income
      4. Higher attendance
      5. Name (alphabetical) - final fallback
    """
    return (
        -calculate_aggregate(student["marks"]),
        -student["marks"].get(TIE_SUBJECT, 0),
        student["income"],
        -student["attendance"],
        student["name"],
    )


def allocate_scholarships(students):
    eligible, rejected = [], []
    for s in students:
        ok, reason = check_eligibility(s)
        if ok:
            eligible.append(s)
        else:
            rejected.append((s["name"], reason))
    eligible.sort(key=ranking_key)
    return eligible, rejected


def print_report(students):
    eligible, rejected = allocate_scholarships(students)
    print("=" * 72)
    print("SCHOLARSHIP RANK LIST")
    print("=" * 72)
    print(f"{'Rank':<5}{'Name':<10}{'Agg%':<8}{TIE_SUBJECT:<7}{'Income':<10}{'Att%':<7}Status")
    print("-" * 72)
    for rank, s in enumerate(eligible, start=1):
        status = "AWARDED" if rank <= TOTAL_SEATS else "WAITLIST"
        print(f"{rank:<5}{s['name']:<10}{calculate_aggregate(s['marks']):<8.2f}"
              f"{s['marks'].get(TIE_SUBJECT, 0):<7}{s['income']:<10}{s['attendance']:<7}{status}")
    print("\nREJECTED APPLICANTS")
    print("-" * 72)
    for name, reason in rejected:
        print(f"{name:<10}-> {reason}")
    return eligible, rejected


if __name__ == "__main__":
    students = [
        {"name": "Asha",  "marks": {"Maths": 90, "Physics": 85, "English": 80}, "attendance": 92, "income": 150000},
        {"name": "Bharat","marks": {"Maths": 85, "Physics": 90, "English": 80}, "attendance": 88, "income": 120000},
        {"name": "Charan","marks": {"Maths": 95, "Physics": 80, "English": 80}, "attendance": 90, "income": 200000},
        {"name": "Divya", "marks": {"Maths": 90, "Physics": 85, "English": 80}, "attendance": 92, "income": 100000},
        {"name": "Esha",  "marks": {"Maths": 95, "Physics": 95, "English": 35}, "attendance": 95, "income": 100000},
        {"name": "Farid", "marks": {"Maths": 70, "Physics": 65, "English": 60}, "attendance": 70, "income": 100000},
        {"name": "Gita",  "marks": {"Maths": 95, "Physics": 95, "English": 95}, "attendance": 95, "income": 500000},
        {"name": "Hari",  "marks": {"Maths": 50, "Physics": 55, "English": 60}, "attendance": 90, "income": 100000},
        {"name": "Indu",  "marks": {"Maths": 80, "Physics": 80, "English": 80}, "attendance": 85, "income": 250000},
    ]
    print_report(students)