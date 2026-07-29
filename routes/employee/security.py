from flask import (
    render_template,
    redirect,
    url_for,
    session,
    request,
    flash,
    abort
)

from database.database import db

from models.user import User
from models.role import Role

from utils.security import hash_password


# =====================================================
# Reset Password
# =====================================================

def reset_password(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "Super Admin":
        abort(403)

    employee = User.query.get_or_404(id)

    if request.method == "POST":

        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template(
                "employees/reset_password.html",
                employee=employee
            )

        employee.password = hash_password(password)
        employee.updated_by = session.get("username")

        db.session.commit()

        flash("Password reset successfully.", "success")

        return redirect(
            url_for(
                "employee.view_employee",
                id=employee.id
            )
        )

    return render_template(
        "employees/reset_password.html",
        employee=employee
    )


# =====================================================
# Deactivate Employee
# =====================================================

def deactivate_employee(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "Super Admin":
        abort(403)

    employee = User.query.get_or_404(id)

    # Cannot deactivate yourself
    if employee.id == session.get("user_id"):
        flash("You cannot deactivate your own account.", "danger")
        return redirect(
            url_for("employee.view_employee", id=id)
        )

    # Prevent deactivating the last active Super Admin
    if employee.role and employee.role.name == "Super Admin":

        active_admins = User.query.filter_by(
            role_id=employee.role_id,
            active=True
        ).count()

        if active_admins <= 1:
            flash(
                "The last active Super Admin cannot be deactivated.",
                "danger"
            )
            return redirect(
                url_for("employee.view_employee", id=id)
            )

    employee.active = False
    employee.updated_by = session.get("username")

    db.session.commit()

    flash("Employee has been deactivated.", "success")

    return redirect(
        url_for("employee.view_employee", id=id)
    )


# =====================================================
# Activate Employee
# =====================================================

def activate_employee(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    if session.get("role") != "Super Admin":
        abort(403)

    employee = User.query.get_or_404(id)

    employee.active = True
    employee.updated_by = session.get("username")

    db.session.commit()

    flash("Employee has been activated.", "success")

    return redirect(
        url_for("employee.view_employee", id=id)
    )