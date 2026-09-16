from datetime import datetime

from flask import (
    render_template,
    redirect,
    url_for,
    session,
    request,
    flash
)

from database.database import db

from models.user import User
from models.role import Role

from utils.employee_number import generate_employee_number
from utils.security import hash_password


def add_employee():

    if "user_id" not in session:
        return redirect(url_for("login"))

    roles = (
        Role.query
        .order_by(Role.name)
        .all()
    )

    if request.method == "POST":

        username = request.form.get("username", "").strip()

        # Check for duplicate username before creating the employee
        if User.query.filter_by(username=username).first():
            flash(
                "Username already exists. Please choose a different username.",
                "danger"
            )

            return render_template(
                "employees/add.html",
                employee_number=generate_employee_number(),
                roles=roles
            )

        hire_date = None

        hire_date_value = request.form.get("hire_date")

        if hire_date_value:
            hire_date = datetime.strptime(
                hire_date_value,
                "%Y-%m-%d"
            ).date()

        email = request.form.get("email", "").strip()

        if email == "":
            email = None

        employee = User(

            employee_number=generate_employee_number(),

            first_name=request.form.get("first_name"),
            middle_name=request.form.get("middle_name"),
            last_name=request.form.get("last_name"),

            username=username,

            password=hash_password(
                request.form.get("password")
            ),

            email=email,
            phone=request.form.get("phone"),

            department=request.form.get("department"),

            hire_date=hire_date,

            role_id=int(request.form.get("role_id")),

            active=request.form.get("active") == "1"

        )

        try:

            db.session.add(employee)
            db.session.commit()

        except Exception:

            db.session.rollback()

            flash(
                "Unable to create the employee. Please check the information and try again.",
                "danger"
            )

            return render_template(
                "employees/add.html",
                employee_number=generate_employee_number(),
                roles=roles
            )

        flash(
            "Employee created successfully.",
            "success"
        )

        return redirect(
            url_for("employee.employee_list")
        )

    return render_template(
        "employees/add.html",
        employee_number=generate_employee_number(),
        roles=roles
    )
