from datetime import date, datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from models import attendance_model

attendance_bp = Blueprint("attendance", __name__, url_prefix="/attendance")


def parse_date(text):
    """Turn 'YYYY-MM-DD' into a date, or return None if invalid."""
    try:
        return datetime.strptime(text, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


@attendance_bp.route("/mark", methods=["GET", "POST"])
def mark():
    today = date.today()

    if request.method == "POST":
        selected = parse_date(request.form.get("attendance_date"))
        if selected is None:
            flash("Please choose a valid date.", "danger")
            return redirect(url_for("attendance.mark"))
        if selected > today:
            flash("You cannot mark attendance for a future date.", "danger")
            return redirect(url_for("attendance.mark"))

        students = attendance_model.get_marking_sheet(selected)
        if not students:
            flash("Add some students before marking attendance.", "warning")
            return redirect(url_for("students.list_students"))

        records = []
        for student in students:
            status = request.form.get(f"status_{student['student_id']}")
            if status not in ("Present", "Absent"):
                flash(f"Please choose Present or Absent for {student['full_name']}.", "danger")
                return redirect(url_for("attendance.mark", date=selected.isoformat()))
            records.append((student["student_id"], status))

        attendance_model.save_attendance(selected, records)
        flash(f"Attendance saved for {selected.strftime('%d %b %Y')}.", "success")
        return redirect(url_for("attendance.mark", date=selected.isoformat()))

    # GET request: show the form for the chosen date (default: today)
    selected = parse_date(request.args.get("date")) or today
    if selected > today:
        flash("Future dates are not allowed. Showing today instead.", "warning")
        selected = today

    students = attendance_model.get_marking_sheet(selected)
    already_marked = any(s["status"] is not None for s in students)

    return render_template(
        "attendance/mark.html",
        students=students,
        selected_date=selected.isoformat(),
        display_date=selected.strftime("%A, %d %B %Y"),
        max_date=today.isoformat(),
        already_marked=already_marked,
    )


@attendance_bp.route("/history")
def history():
    today = date.today()
    requested = request.args.get("date")
    selected = parse_date(requested)

    if requested and selected is None:
        flash("That date was not valid. Showing the latest date instead.", "warning")

    if selected is None:
        selected = attendance_model.get_latest_date() or today

    records = attendance_model.get_history(selected)
    present = sum(1 for r in records if r["status"] == "Present")
    absent = len(records) - present

    return render_template(
        "attendance/history.html",
        records=records,
        present=present,
        absent=absent,
        selected_date=selected.isoformat(),
        display_date=selected.strftime("%A, %d %B %Y"),
        max_date=today.isoformat(),
    )