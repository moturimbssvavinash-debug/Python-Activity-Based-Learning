# University Admission Decision Engine

# ---------- Course rules (change here to change policy) ----------
COURSES = {
    "CSE": {   # B.Tech Computer Science
        "required": {"Maths": 60, "Physics": 50, "English": 40},  # subject: minimum marks
        "cutoff": 70.0,          # minimum aggregate %
        "seats": 3,
        "primary": "Maths",      # subject used for tie-break 1
    },
    "PHY": {   # B.Sc Physics
        "required": {"Maths": 50, "Physics": 60},
        "cutoff": 60.0,
        "seats": 2,
        "primary": "Physics",
    },
    "COM": {   # B.Com
        "required": {"Accountancy": 50, "English": 40},
        "cutoff": 55.0,
        "seats": 2,
        "primary": "Accountancy",
    },
}


def calculate_aggregate(marks):
    """Average of all subject marks (each out of 100)."""
    return sum(marks.values()) / len(marks)


def check_eligibility(candidate):
    """Return (True, '') if eligible, else (False, reason)."""
    course = COURSES.get(candidate["course"])
    if course is None:
        return False, f"Unknown course '{candidate['course']}'"

    # 1. Subject eligibility: subject must exist AND meet its minimum
    for subject, minimum in course["required"].items():
        if subject not in candidate["marks"]:
            return False, f"Required subject {subject} not studied"
        if candidate["marks"][subject] < minimum:
            return False, f"{subject} {candidate['marks'][subject]} < {minimum}"

    # 2. Aggregate vs course cutoff
    agg = calculate_aggregate(candidate["marks"])
    if agg < course["cutoff"]:
        return False, f"Aggregate {agg:.2f}% < cutoff {course['cutoff']}%"
    return True, ""


def ranking_key(candidate):
    """
    Sort key (smallest first, so negate 'higher is better' values).
    Tie-break order:
      1. Higher aggregate
      2. Higher marks in the course's primary subject
      3. Higher entrance test score
      4. Older candidate (earlier date of birth)
      5. Name (alphabetical) - final fallback
    """
    course = COURSES[candidate["course"]]
    return (
        -calculate_aggregate(candidate["marks"]),
        -candidate["marks"][course["primary"]],
        -candidate["entrance"],
        candidate["dob"],            # "YYYY-MM-DD": earlier date sorts first
        candidate["name"],
    )


def run_admission(candidates):
    """Return {course: {'ranked': [...], 'rejected': [...]}}"""
    result = {c: {"ranked": [], "rejected": []} for c in COURSES}
    unknown = []
    for cand in candidates:
        ok, reason = check_eligibility(cand)
        if cand["course"] not in COURSES:
            unknown.append((cand["name"], reason))
        elif ok:
            result[cand["course"]]["ranked"].append(cand)
        else:
            result[cand["course"]]["rejected"].append((cand["name"], reason))
    for course in result:
        result[course]["ranked"].sort(key=ranking_key)
    return result, unknown


def print_report(candidates):
    result, unknown = run_admission(candidates)
    for code, data in result.items():
        info = COURSES[code]
        print("=" * 76)
        print(f"COURSE: {code}   Seats: {info['seats']}   Cutoff: {info['cutoff']}%   "
              f"Tie-break subject: {info['primary']}")
        print("=" * 76)
        print(f"{'Rank':<5}{'Name':<9}{'Agg%':<8}{info['primary'][:7]:<9}{'Entrance':<10}{'DOB':<12}Status")
        print("-" * 76)
        if not data["ranked"]:
            print("(no eligible candidates)")
        for rank, c in enumerate(data["ranked"], start=1):
            status = "ADMITTED" if rank <= info["seats"] else "WAITLIST"
            print(f"{rank:<5}{c['name']:<9}{calculate_aggregate(c['marks']):<8.2f}"
                  f"{c['marks'][info['primary']]:<9}{c['entrance']:<10}{c['dob']:<12}{status}")
        if data["rejected"]:
            print("\nRejected:")
            for name, reason in data["rejected"]:
                print(f"  {name:<9}-> {reason}")
        print()
    for name, reason in unknown:
        print(f"Invalid application: {name} -> {reason}")


if __name__ == "__main__":
    candidates = [
        # ---- CSE ----
        {"name": "Arun",   "course": "CSE", "marks": {"Maths": 90, "Physics": 80, "English": 70}, "entrance": 88, "dob": "2006-03-10"},
        {"name": "Bhavna", "course": "CSE", "marks": {"Maths": 90, "Physics": 70, "English": 80}, "entrance": 92, "dob": "2006-05-01"},
        {"name": "Chetan", "course": "CSE", "marks": {"Maths": 85, "Physics": 85, "English": 70}, "entrance": 80, "dob": "2006-01-20"},
        {"name": "Deepa",  "course": "CSE", "marks": {"Maths": 90, "Physics": 80, "English": 70}, "entrance": 88, "dob": "2005-12-15"},
        {"name": "Eswar",  "course": "CSE", "marks": {"Maths": 55, "Physics": 95, "English": 90}, "entrance": 90, "dob": "2006-02-02"},
        {"name": "Farah",  "course": "CSE", "marks": {"Maths": 65, "Physics": 60, "English": 70}, "entrance": 75, "dob": "2006-07-07"},
        {"name": "Gopal",  "course": "CSE", "marks": {"Maths": 95, "English": 90},                "entrance": 85, "dob": "2006-04-04"},
        # ---- PHY ----
        {"name": "Hema",   "course": "PHY", "marks": {"Maths": 70, "Physics": 80, "Chemistry": 75}, "entrance": 70, "dob": "2006-06-06"},
        {"name": "Imran",  "course": "PHY", "marks": {"Maths": 80, "Physics": 70, "Chemistry": 75}, "entrance": 65, "dob": "2006-08-08"},
        {"name": "Jaya",   "course": "PHY", "marks": {"Maths": 60, "Physics": 55, "Chemistry": 70}, "entrance": 60, "dob": "2006-09-09"},
        # ---- COM ----
        {"name": "Kavya",  "course": "COM", "marks": {"Accountancy": 80, "English": 60, "Economics": 70}, "entrance": 72, "dob": "2006-02-14"},
        {"name": "Lokesh", "course": "COM", "marks": {"Accountancy": 45, "English": 90, "Economics": 90}, "entrance": 80, "dob": "2006-03-03"},
        {"name": "Meena",  "course": "COM", "marks": {"Accountancy": 55, "English": 50, "Economics": 50}, "entrance": 50, "dob": "2006-10-10"},
        # ---- Invalid course ----
        {"name": "Naveen", "course": "MBA", "marks": {"Maths": 90, "English": 90}, "entrance": 80, "dob": "2006-01-01"},
    ]
    print_report(candidates)