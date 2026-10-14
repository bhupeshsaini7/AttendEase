"""All SQL related to students."""
from db import execute, fetch_all, fetch_one


def get_students_with_stats(search=""):
    """Return every student with attendance statistics.

    Percentage = present days / total recorded days * 100.
    A student with no records gets 0 (and total_days = 0), so there is no divide-by-zero.
    """
    sql = """
        SELECT
            s.student_id,
            s.roll_number,
            s.full_name,
            s.email,
            s.class_name,
            COUNT(a.attendance_id) AS total_days,
            COALESCE(SUM(a.status = 'Present'), 0) AS present_days,
            COALESCE(SUM(a.status = 'Absent'), 0) AS absent_days,
            CASE
                WHEN COUNT(a.attendance_id) = 0 THEN 0
                ELSE ROUND(SUM(a.status = 'Present') * 100 / COUNT(a.attendance_id), 1)
            END AS percentage
        FROM students s
        LEFT JOIN attendance a ON a.student_id = s.student_id
    """
    params = ()
    if search:
        sql += """
            WHERE s.full_name LIKE %s
               OR s.roll_number LIKE %s
               OR s.class_name LIKE %s
        """
        like = f"%{search}%"
        params = (like, like, like)

    sql += """
        GROUP BY s.student_id, s.roll_number, s.full_name, s.email, s.class_name
        ORDER BY s.roll_number
    """
    return fetch_all(sql, params)


def get_student(student_id):
    return fetch_one("SELECT * FROM students WHERE student_id = %s", (student_id,))


def count_students():
    row = fetch_one("SELECT COUNT(*) AS total FROM students")
    return row["total"]


def add_student(roll_number, full_name, email, class_name):
    return execute(
        """INSERT INTO students (roll_number, full_name, email, class_name)
           VALUES (%s, %s, %s, %s)""",
        (roll_number, full_name, email, class_name),
    )


def update_student(student_id, roll_number, full_name, email, class_name):
    return execute(
        """UPDATE students
           SET roll_number = %s, full_name = %s, email = %s, class_name = %s
           WHERE student_id = %s""",
        (roll_number, full_name, email, class_name, student_id),
    )


def delete_student(student_id):
    return execute("DELETE FROM students WHERE student_id = %s", (student_id,))