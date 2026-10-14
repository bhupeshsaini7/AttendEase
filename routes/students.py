import re

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from mysql.connector import IntegrityError

from models import student_model

students_bp = Blueprint("students", __name__, url_prefix="/students")

ROLL_PATTERN = re.compile(r"^[A-Za-z0-9/-]+$")
NAME_PATTERN = re.compile(r"^[A-Za-z][A-Za-z .'-]*$")
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def clean_form(form):
    """Clean the submitted form and check it. Returns (data, errors)."""
    data = {
        "roll_number": form.get("roll_number", "").strip(),
        "full_name": " ".join(form.get("full_name", "").split()),
        "email": form.get("email", "").strip().lower(),
        "class_name": form.get("class_name", "").strip(),
    }
    errors = []

    if not data["roll_number"]:
        errors.append("Roll number is required.")
    elif len(data["roll_number"]) > 20:
        errors.append("Roll number must be 20 characters or fewer.")
    elif not ROLL_PATTERN.match(data["roll_number"]):
        errors.append("Roll number can only contain letters, numbers, '-' and '/'.")

    if not data["full_name"]:
        errors.append("Full name is required.")
    elif len(data["full_name"]) > 100:
        errors.append("Full name must be 100 characters or fewer.")
    elif not NAME_PATTERN.match(data["full_name"]):
        errors.append("Full name can only contain letters, spaces, '.', ''' and '-'.")

    if not data["email"]:
        errors.append("Email is required.")
    elif len(data["email"]) > 100:
        errors.append("Email must be 100 characters or fewer.")
    elif not EMAIL_PATTERN.match(data["email"]):
        errors.append("Please enter a valid email address.")

    if not data["class_name"]:
        errors.append("Class is required.")
    elif len(data["class_name"]) > 50:
        errors.append("Class must be 50 characters or fewer.")

    return data, errors


def duplicate_message(error):
    """Turn MySQL's duplicate-key error into a friendly sentence."""
    text = str(error)
    if "uq_students_roll_number" in text:
        return "A student with this roll number already exists."
    if "uq_students_email" in text:
        return "A student with this email already exists."
    return "This student already exists."


@students_bp.route("/")
def list_students():
    search = request.args.get("search", "").strip()
    students = student_model.get_students_with_stats(search)
    return render_template("students/list.html", students=students, search=search)


@students_bp.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        data, errors = clean_form(request.form)
        if not errors:
            try:
                student_model.add_student(**data)
                flash("Student added successfully.", "success")
                return redirect(url_for("students.list_students"))
            except IntegrityError as error:
                if error.errno != 1062:  # 1062 = duplicate entry
                    raise
                errors.append(duplicate_message(error))
        return render_template("students/form.html", form=data, errors=errors, mode="add")

    return render_template("students/form.html", form={}, errors=[], mode="add")


@students_bp.route("/<int:student_id>/edit", methods=["GET", "POST"])
def edit_student(student_id):
    student = student_model.get_student(student_id)
    if student is None:
        abort(404)

    if request.method == "POST":
        data, errors = clean_form(request.form)
        if not errors:
            try:
                student_model.update_student(student_id, **data)
                flash("Student updated successfully.", "success")
                return redirect(url_for("students.list_students"))
            except IntegrityError as error:
                if error.errno != 1062:
                    raise
                errors.append(duplicate_message(error))
        return render_template("students/form.html", form=data, errors=errors, mode="edit")

    return render_template("students/form.html", form=student, errors=[], mode="edit")


@students_bp.route("/<int:student_id>/delete", methods=["POST"])
def delete_student(student_id):
    if student_model.get_student(student_id) is None:
        abort(404)
    student_model.delete_student(student_id)
    flash("Student deleted.", "success")
    return redirect(url_for("students.list_students"))