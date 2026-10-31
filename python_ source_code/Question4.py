# Examination Result and Grace-Mark Validation  

MAX_MARKS = 100          
PASS_MARK = 40           
PASS_GRACE_LIMIT = 5     
MAX_FAILED = 2           
MAX_TOTAL_GRACE = 10     
MAX_SUBJECT_GRACE = 5    
CLASS_GRACE_LIMIT = 5    


CLASSES = [(75, "Distinction"), (60, "First Class"), (50, "Second Class")]


def is_valid(marks):
    """All marks must be whole numbers from 0 to 100."""
    for mark in marks.values():
        if not isinstance(mark, int) or mark < 0 or mark > MAX_MARKS:
            return False
    return True


def get_class(percent):
    for limit, name in CLASSES:
        if percent >= limit:
            return name
    return "Pass Class"


def give_pass_grace(marks):
    """Step 1: raise failed subjects to 40. Returns grace dict, or None if not allowed."""
    grace = {subject: 0 for subject in marks}
    failed = [s for s in marks if marks[s] < PASS_MARK]

    if len(failed) > MAX_FAILED:
        return None
    for s in failed:
        need = PASS_MARK - marks[s]
        if need > PASS_GRACE_LIMIT:
            return None
        grace[s] = need
    if sum(grace.values()) > MAX_TOTAL_GRACE:
        return None
    return grace


def give_class_grace(marks, grace):
    """Step 2: if a few marks short of the next class, add grace to ONE subject."""
    total = sum(marks.values()) + sum(grace.values())
    max_total = MAX_MARKS * len(marks)

    
    for limit, name in reversed(CLASSES):            
        boundary = limit * max_total // 100           
        if total < boundary:
            shortfall = boundary - total
            break
    else:
        return grace                                  

    if shortfall > CLASS_GRACE_LIMIT:
        return grace
    if sum(grace.values()) + shortfall > MAX_TOTAL_GRACE:
        return grace

    
    for s in sorted(marks, key=lambda x: marks[x] + grace[x]):
        new_mark = marks[s] + grace[s] + shortfall
        new_grace = grace[s] + shortfall
        if new_mark <= MAX_MARKS and new_grace <= MAX_SUBJECT_GRACE:
            grace[s] = new_grace
            return grace
    return grace                                    


def process(name, marks):
    if not is_valid(marks):
        return [name, "-", "-", "-", "-", "INVALID", "-"]

    grace = give_pass_grace(marks)
    if grace is None:
        total = sum(marks.values())
        return [name, total, 0, total, f"{total * 100 / (MAX_MARKS * len(marks)):.1f}", "FAIL", "-"]

    grace = give_class_grace(marks, grace)
    original = sum(marks.values())
    used = sum(grace.values())
    final = original + used
    percent = final * 100 / (MAX_MARKS * len(marks))
    return [name, original, used, final, f"{percent:.1f}", "PASS", get_class(percent)]


if __name__ == "__main__":
    subjects = ["Maths", "Physics", "Chemistry", "English", "CompSci"]
    data = [
        ("Priya",  [80, 85, 78, 90, 72]),
        ("Suma",   [36, 64, 64, 64, 65]),
        ("Tarun",  [38, 39, 60, 70, 80]),
        ("Uma",    [35, 35, 35, 70, 70]),
        ("Vikram", [30, 80, 80, 80, 80]),
        ("Wasim",  [100, 100, 70, 60, 43]),
        ("Meera",  [36, 36, 72, 72, 73]),
        ("Yash",   [100, 100, 100, 100, 100]),
        ("Arjun",  [105, 70, 70, 70, 70]),
    ]

    print("EXAMINATION RESULTS (max 500 marks, pass mark 40 per subject)")
    print("-" * 66)
    print(f"{'Name':<8}{'Original':<10}{'Grace':<7}{'Final':<7}{'%':<7}{'Result':<9}Class")
    print("-" * 66)
    for name, m in data:
        row = process(name, dict(zip(subjects, m)))
        print(f"{row[0]:<8}{row[1]:<10}{row[2]:<7}{row[3]:<7}{row[4]:<7}{row[5]:<9}{row[6]}")
        