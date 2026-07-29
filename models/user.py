from database.database import db


class User(db.Model):
    __tablename__ = "users"

    # ============================================
    # Primary Key
    # ============================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ============================================
    # Employee Information
    # ============================================

    employee_number = db.Column(
        db.String(20),
        unique=True
    )

    first_name = db.Column(
        db.String(50),
        nullable=False
    )

    middle_name = db.Column(
        db.String(50)
    )

    last_name = db.Column(
        db.String(50),
        nullable=False
    )

    # ============================================
    # Login Information
    # ============================================

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    # ============================================
    # Contact Information
    # ============================================

    email = db.Column(
        db.String(120),
        unique=True
    )

    phone = db.Column(
        db.String(20)
    )

    # ============================================
    # Employment Information
    # ============================================

    department = db.Column(
        db.String(50)
    )

    hire_date = db.Column(
        db.Date
    )

    # ============================================
    # Role
    # ============================================

    role_id = db.Column(
        db.Integer,
        db.ForeignKey("roles.id")
    )

    role = db.relationship(
        "Role",
        back_populates="users"
    )

    # ============================================
    # Status
    # ============================================

    active = db.Column(
        db.Boolean,
        default=True,
        nullable=False
    )

    # ============================================
    # Audit Information
    # ============================================

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )

    updated_at = db.Column(
        db.DateTime,
        onupdate=db.func.now()
    )

    updated_by = db.Column(
        db.String(50)
    )

    last_login = db.Column(
        db.DateTime
    )

    # ============================================
    # Display Name
    # ============================================

    @property
    def full_name(self):

        parts = [
            self.first_name,
            self.middle_name,
            self.last_name
        ]

        return " ".join(
            part for part in parts if part
        )

    def __repr__(self):

        return f"<User {self.username}>"