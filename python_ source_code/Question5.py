# Student Timetable Conflict Detection

VALID_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]


def time_to_minutes(t):
    """Convert 'HH:MM' string to minutes since midnight."""
    hours, minutes = t.split(":")
    return int(hours) * 60 + int(minutes)


def is_overlap(start1, end1, start2, end2):
    """Two periods overlap if each starts before the other ends."""
    s1, e1 = time_to_minutes(start1), time_to_minutes(end1)
    s2, e2 = time_to_minutes(start2), time_to_minutes(end2)
    return s1 < e2 and s2 < e1


def find_overlaps(timetable):
    """Return every pair of classes that overlap in time on the same day."""
    result = []
    for i in range(len(timetable)):
        for j in range(i + 1, len(timetable)):
            a, b = timetable[i], timetable[j]
            if a[1] == b[1] and is_overlap(a[2], a[3], b[2], b[3]):
                result.append((a, b))
    return result


def find_room_conflicts(timetable):
    """Overlapping classes that also use the same room."""
    return [(a, b) for a, b in find_overlaps(timetable) if a[4] == b[4]]


def unavailable_rooms(timetable, day, start, end):
    """Set of rooms that are busy during the requested period."""
    busy = set()
    for course, d, s, e, room in timetable:
        if d == day and is_overlap(start, end, s, e):
            busy.add(room)
    return busy


def validate_timetable(timetable, rooms):
    """Check a proposed timetable. Returns (is_valid, list_of_errors)."""
    errors = []
    for entry in timetable:
        if len(entry) != 5:
            errors.append(f"Bad format: {entry}")
            continue
        course, day, start, end, room = entry
        if day not in VALID_DAYS:
            errors.append(f"{course}: invalid day '{day}'")
        try:
            if time_to_minutes(start) >= time_to_minutes(end):
                errors.append(f"{course}: start time must be before end time")
        except ValueError:
            errors.append(f"{course}: invalid time format")
        if room not in rooms:
            errors.append(f"{course}: unknown room '{room}'")
    if not errors:
        for a, b in find_room_conflicts(timetable):
            errors.append(f"Room clash: {a[0]} and {b[0]} in {a[4]} on {a[1]}")
    return len(errors) == 0, errors


if __name__ == "__main__":
    rooms = ["R101", "R102", "Lab1"]
    timetable = [
        ("Maths",   "Mon", "09:00", "10:00", "R101"),
        ("Physics", "Mon", "09:30", "10:30", "R101"),
        ("Chem",    "Mon", "09:45", "11:00", "Lab1"),
        ("English", "Tue", "10:00", "11:00", "R102"),
    ]
    print("Overlapping classes:")
    for a, b in find_overlaps(timetable):
        print(" ", a[0], "<->", b[0])
    print("Room conflicts:")
    for a, b in find_room_conflicts(timetable):
        print(" ", a[0], "<->", b[0], "in", a[4])
    print("Busy rooms Mon 09:00-10:00:", sorted(unavailable_rooms(timetable, "Mon", "09:00", "10:00")))
    ok, errs = validate_timetable(timetable, rooms)
    print("Valid?", ok)
    for e in errs:
        print(" -", e)
        