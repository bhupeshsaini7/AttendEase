"""All SQL related to attendance."""
from db import execute_many, fetch_all, fetch_one


def get_marking_sheet(attendance_date):
    """All students, plus their saved status for that date (None if not marked yet)."""
    return fetch_all(
        """
        SELECT s.student_id, s.roll_number, s.full_name, s.class_name, a.status
        FROM students s
        LEFT JOIN attendance a
               ON a.student_id = s.student_id
              AND a.attendance_date = %s
        ORDER BY s.roll_number
        """,
        (attendance_date,),
    )


def save_attendance(attendance_date, records):
    """Save a list of (student_id, status) for one date.

    The UNIQUE (student_id, attendance_date) key guarantees no duplicates.
    If a record already exists, ON DUPLICATE KEY UPDATE changes its status
    instead of creating a second row, so you can correct a mistake.
    """
    sql = """
        INSERT INTO attendance (student_id, attendance_date, status)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE status = VALUES(status)
    """
    params_list = [(student_id, attendance_date, status) for student_id, status in records]
    execute_many(sql, params_list)


def get_history(attendance_date):
    """All attendance records for one date."""
    return fetch_all(
        """
        SELECT s.roll_number, s.full_name, s.class_name, a.status
        FROM attendance a
        JOIN students s ON s.student_id = a.student_id
        WHERE a.attendance_date = %s
        ORDER BY s.roll_number
        """,
        (attendance_date,),
    )


def get_latest_date():
    """Most recent date that has any records (or None)."""
    row = fetch_one("SELECT MAX(attendance_date) AS latest FROM attendance")
    return row["latest"]


def get_day_summary(attendance_date):
    """Counts of records and present students for one date."""
    row = fetch_one(
        """
        SELECT COUNT(*) AS total,
               COALESCE(SUM(status = 'Present'), 0) AS present
        FROM attendance
        WHERE attendance_date = %s
        """,
        (attendance_date,),
    )
    return {"total": int(row["total"]), "present": int(row["present"])}


def get_overall_summary():
    """Counts across ALL attendance records."""
    row = fetch_one(
        """
        SELECT COUNT(*) AS total,
               COALESCE(SUM(status = 'Present'), 0) AS present
        FROM attendance
        """
    )
    return {"total": int(row["total"]), "present": int(row["present"])}


def get_recent_daily_percentages(limit=7):
    """Attendance % for the most recent dates that have records (oldest first)."""
    rows = fetch_all(
        """
        SELECT attendance_date,
               ROUND(SUM(status = 'Present') * 100 / COUNT(*), 1) AS percentage
        FROM attendance
        GROUP BY attendance_date
        ORDER BY attendance_date DESC
        LIMIT %s
        """,
        (limit,),
    )
    rows.reverse()  # oldest first, so the chart reads left to right
    return rows