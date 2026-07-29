from models.user import User
from models.role import Role

from database.database import db

from utils.security import hash_password


def seed_super_admin():

    existing = User.query.filter_by(
        username="dtracer1"
    ).first()

    if existing:

        print("Super Admin already exists.")

        return

    super_admin_role = Role.query.filter_by(
        name="Super Admin"
    ).first()

    if super_admin_role is None:

        print("Super Admin role not found.")

        return

    user = User(

        employee_number="000001",

        first_name="Dennis",

        middle_name="",

        last_name="Ebora",

        username="dtracer1",

        email="",

        phone="",

        department="Administration",

        hire_date=None,

        password=hash_password("12345678"),

        role=super_admin_role,

        active=True

    )

    db.session.add(user)

    db.session.commit()

    print("Super Admin created successfully.")