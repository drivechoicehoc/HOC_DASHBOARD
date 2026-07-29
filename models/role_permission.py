from database.database import db


class RolePermission(db.Model):
    __tablename__ = "role_permissions"

    id = db.Column(db.Integer, primary_key=True)

    role_id = db.Column(
        db.Integer,
        db.ForeignKey("roles.id"),
        nullable=False,
        unique=True
    )

    dashboard = db.Column(db.Boolean, default=False)

    new_bdc_request = db.Column(db.Boolean, default=False)

    bdc_request_queue = db.Column(db.Boolean, default=False)

    delete_bdc_request = db.Column(db.Boolean, default=False)

    employee_management = db.Column(db.Boolean, default=False)

    reports = db.Column(db.Boolean, default=False)

    settings = db.Column(db.Boolean, default=False)