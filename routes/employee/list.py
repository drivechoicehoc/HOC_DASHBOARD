from flask import (
    render_template,
    redirect,
    url_for,
    session,
    request
)

from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from models.user import User
from models.role import Role
from datetime import timezone
from zoneinfo import ZoneInfo


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

    cleveland_tz = ZoneInfo("America/New_York")

    for employee in employees:
        if employee.last_login:
            employee.last_login = (
                employee.last_login
                .replace(tzinfo=timezone.utc)
                .astimezone(cleveland_tz)
            )

    return render_template(
        "employees/list.html",
        employees=employees,
        roles=roles,
        search=search,
        selected_department=department,
        selected_role=role
    )