from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    request,
    abort,
    flash
)

from utils.decorators import permission_required
from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from database.database import db

from models.user import User
from models.role import Role

from utils.employee_number import generate_employee_number
from utils.security import hash_password


employee_bp = Blueprint(
    "employee",
    __name__
)


# =====================================================
# Employee List
# =====================================================

@employee_bp.route("/employees")
@permission_required("employee_management")
def employee_list():

    if "user_id" not in session:
        return redirect(url_for("login"))

    search = request.args.get("search", "").strip()
    department = request.args.get("department", "").strip()
    role = request.args.get("role", "").strip()

    roles = (
        Role.query
        .order_by(Role.name)
        .all()
    )

    query = (
        User.query
        .options(joinedload(User.role))
    )

    # -----------------------------------------
    # Search
    # -----------------------------------------

    if search:

        query = query.filter(

            or_(

                User.employee_number.ilike(f"%{search}%"),

                User.first_name.ilike(f"%{search}%"),

                User.middle_name.ilike(f"%{search}%"),

                User.last_name.ilike(f"%{search}%"),

                User.username.ilike(f"%{search}%")

            )

        )

    # -----------------------------------------
    # Department Filter
    # -----------------------------------------

    if department:

        query = query.filter(
            User.department == department
        )

    # -----------------------------------------
    # Role Filter
    # -----------------------------------------

    if role:

        query = query.join(Role).filter(
            Role.id == int(role)
        )

    employees = (
        query
        .order_by(User.employee_number)
        .all()
    )

    return render_template(
        "employees/list.html",
        employees=employees,
        roles=roles,
        search=search,
        selected_department=department,
        selected_role=role
    )


# =====================================================
# View Employee
# =====================================================

@employee_bp.route("/employees/<int:id>")
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


# =====================================================
# Add Employee
# =====================================================

@employee_bp.route("/employees/add", methods=["GET", "POST"])
def add_employee():

    if "user_id" not in session:
        return redirect(url_for("login"))

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

        employee = User(

            employee_number=generate_employee_number(),

            first_name=request.form.get("first_name"),
            middle_name=request.form.get("middle_name"),
            last_name=request.form.get("last_name"),

            username=request.form.get("username"),

            password=hash_password(
                request.form.get("password")
            ),

            email=request.form.get("email"),
            phone=request.form.get("phone"),

            department=request.form.get("department"),

            hire_date=hire_date,

            role_id=int(request.form.get("role_id")),

            active=request.form.get("active") == "1"

        )

        db.session.add(employee)
        db.session.commit()

        return redirect(
            url_for("employee.employee_list")
        )

    return render_template(
        "employees/add.html",
        employee_number=generate_employee_number(),
        roles=roles
    )


# =====================================================
# Edit Employee
# =====================================================

@employee_bp.route("/employees/edit/<int:id>", methods=["GET", "POST"])
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

        employee.first_name = request.form.get("first_name")
        employee.middle_name = request.form.get("middle_name")
        employee.last_name = request.form.get("last_name")

        employee.email = request.form.get("email")
        employee.phone = request.form.get("phone")

        employee.department = request.form.get("department")

        employee.hire_date = hire_date

        employee.role_id = int(request.form.get("role_id"))

        employee.active = request.form.get("active") == "1"

        employee.updated_by = session.get("username")

        db.session.commit()

        return redirect(
            url_for("employee.view_employee", id=employee.id)
        )

    return render_template(
        "employees/edit.html",
        employee=employee,
        roles=roles
    )


# =====================================================
# Reset Password
# =====================================================

@employee_bp.route("/employees/reset-password/<int:id>", methods=["GET", "POST"])
def reset_password(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    # Only Super Admin can reset passwords
    if session.get("role") != "Super Admin":
        abort(403)

    employee = User.query.get_or_404(id)

    if request.method == "POST":

        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        if password != confirm_password:

            flash(
                "Passwords do not match.",
                "danger"
            )

            return render_template(
                "employees/reset_password.html",
                employee=employee
            )

        employee.password = hash_password(password)

        employee.updated_by = session.get("username")

        db.session.commit()

        flash(
            "Password has been reset successfully.",
            "success"
        )

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
# Delete Employee
# =====================================================

@employee_bp.route("/employees/delete/<int:id>", methods=["GET"])
def delete_employee(id):

    return f"Delete Employee: {id}"