from flask import (
    render_template,
    redirect,
    url_for,
    session,
    abort
)

from sqlalchemy.orm import joinedload

from models.user import User


def view_employee(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    employee = (
        User.query
        .options(joinedload(User.role))
        .filter_by(id=id)
        .first()
    )

    if employee is None:
        abort(404)

    return render_template(
        "employees/view.html",
        employee=employee
    )