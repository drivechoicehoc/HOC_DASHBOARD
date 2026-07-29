from models.user import User


def generate_employee_number():

    last_employee = (
        User.query
        .order_by(User.employee_number.desc())
        .first()
    )

    if (
        last_employee is None or
        last_employee.employee_number is None
    ):
        return "000001"

    next_number = int(last_employee.employee_number) + 1

    return f"{next_number:06d}"