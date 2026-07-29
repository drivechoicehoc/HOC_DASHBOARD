from flask import Blueprint

employee_bp = Blueprint(
    "employee",
    __name__
)

from .list import employee_list
from .add import add_employee
from .profile import view_employee
from .edit import edit_employee
from .delete import delete_employee
from .security import (
    reset_password,
    activate_employee,
    deactivate_employee
)

employee_bp.add_url_rule(
    "/employees",
    view_func=employee_list,
    endpoint="employee_list"
)

employee_bp.add_url_rule(
    "/employees/add",
    view_func=add_employee,
    methods=["GET", "POST"],
    endpoint="add_employee"
)

employee_bp.add_url_rule(
    "/employees/<int:id>",
    view_func=view_employee,
    endpoint="view_employee"
)

employee_bp.add_url_rule(
    "/employees/edit/<int:id>",
    view_func=edit_employee,
    methods=["GET", "POST"],
    endpoint="edit_employee"
)

employee_bp.add_url_rule(
    "/employees/reset-password/<int:id>",
    view_func=reset_password,
    methods=["GET", "POST"],
    endpoint="reset_password"
)

employee_bp.add_url_rule(
    "/employees/activate/<int:id>",
    view_func=activate_employee,
    methods=["POST"],
    endpoint="activate_employee"
)

employee_bp.add_url_rule(
    "/employees/deactivate/<int:id>",
    view_func=deactivate_employee,
    methods=["POST"],
    endpoint="deactivate_employee"
)

employee_bp.add_url_rule(
    "/employees/delete/<int:id>",
    view_func=delete_employee,
    methods=["GET"],
    endpoint="delete_employee"
)