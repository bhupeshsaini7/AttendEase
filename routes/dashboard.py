from datetime import date

from flask import Blueprint, render_template

from models import attendance_model, student_model

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
def index():
    today = date.today()
    total_students = student_model.count_students()
    today_summary = attendance_model.get_day_summary(today)
    overall = attendance_model.get_overall_summary()

    if overall["total"] > 0:
        overall_percentage = round(overall["present"] * 100 / overall["total"], 1)
    else:
        overall_percentage = 0

    daily = attendance_model.get_recent_daily_percentages(7)
    chart_labels = [row["attendance_date"].strftime("%d %b") for row in daily]
    chart_values = [float(row["percentage"]) for row in daily]

    return render_template(
        "dashboard.html",
        today_label=today.strftime("%A, %d %B %Y"),
        total_students=total_students,
        today_present=today_summary["present"],
        today_absent=today_summary["total"] - today_summary["present"],
        today_marked=today_summary["total"],
        overall_percentage=overall_percentage,
        chart_labels=chart_labels,
        chart_values=chart_values,
    )