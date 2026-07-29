from flask import (
    redirect,
    url_for,
    session,
    abort,
    flash
)

from database.database import db
from models.user import User


def delete_employee(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    # Only Super Admin can delete employees
    if session.get("role") != "Super Admin":
        abort(403)

    employee = User.query.get_or_404(id)

    # Prevent deleting your own account
    if employee.id == session.get("user_id"):

        flash(
            "You cannot delete your own account.",
            "danger"
        )

        return redirect(
            url_for(
                "employee.view_employee",
                id=employee.id
            )
        )

    db.session.delete(employee)
    db.session.commit()

    flash(
        "Employee deleted successfully.",
        "success"
    )

    return redirect(
        url_for("employee.employee_list")
    )