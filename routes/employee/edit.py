from datetime import datetime

from flask import (
    render_template,
    redirect,
    url_for,
    session,
    request
)

from database.database import db

from models.user import User
from models.role import Role


def edit_employee(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    employee = User.query.get_or_404(id)

    roles = (
        Role.query
        .order_by(Role.name)
        .all()
    )

    if request.method == "POST":

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

        employee.first_name = request.form.get("first_name")
        employee.middle_name = request.form.get("middle_name")
        employee.last_name = request.form.get("last_name")

        employee.email = email
        employee.phone = request.form.get("phone")

        employee.department = request.form.get("department")
        employee.hire_date = hire_date

        employee.role_id = int(request.form.get("role_id"))
        employee.active = request.form.get("active") == "1"

        employee.updated_by = session.get("username")

        db.session.commit()

        return redirect(
            url_for(
                "employee.view_employee",
                id=employee.id
            )
        )

    return render_template(
        "employees/edit.html",
        employee=employee,
        roles=roles
    )