from datetime import datetime

from database.database import db


class BDCRequest(db.Model):
    __tablename__ = "bdc_requests"

    # ============================================
    # Primary Key
    # ============================================

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # ============================================
    # Ticket Information
    # ============================================

    ticket_number = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    started_at = db.Column(
        db.DateTime,
        nullable=True
    )

    completed_at = db.Column(
        db.DateTime,
        nullable=True
    )

    bdc_agent = db.Column(
        db.String(100),
        nullable=False
    )

    # ============================================
    # Request Information
    # ============================================

    request_type = db.Column(
        db.String(100),
        nullable=False
    )

    other_request_type = db.Column(
        db.String(255),
        nullable=True
    )

    # ============================================
    # Customer Information
    # ============================================

    first_name = db.Column(
        db.String(100),
        nullable=False
    )

    middle_name = db.Column(
        db.String(100),
        nullable=True
    )

    last_name = db.Column(
        db.String(100),
        nullable=False
    )

    address = db.Column(
        db.String(255),
        nullable=True
    )

    phone = db.Column(
        db.String(30),
        nullable=True
    )

    email = db.Column(
        db.String(120),
        nullable=True
    )

    # ============================================
    # Assignment
    # ============================================

    sales_rep = db.Column(
        db.String(100),
        nullable=True
    )

    sales_manager = db.Column(
        db.String(100),
        nullable=True
    )

    # ============================================
    # Vehicle Information
    # ============================================

    vehicle_year = db.Column(
        db.String(4),
        nullable=True
    )

    vehicle_make = db.Column(
        db.String(50),
        nullable=True
    )

    vehicle_model = db.Column(
        db.String(100),
        nullable=True
    )

    vehicle_trim = db.Column(
        db.String(100),
        nullable=True
    )

    stock_number = db.Column(
        db.String(30),
        nullable=True
    )

    vin = db.Column(
        db.String(30),
        nullable=True
    )

    # ============================================
    # BDC Internal Notes
    # ============================================

    bdc_internal_notes = db.Column(
        db.Text,
        nullable=True
    )

    # ============================================
    # Resolution
    # ============================================

    resolution = db.Column(
        db.Text,
        nullable=True
    )

    # ============================================
    # Status
    # ============================================

    status = db.Column(
        db.String(30),
        default="In Progress",
        nullable=False
    )

    # ============================================
    # Audit Information
    # ============================================

    updated_at = db.Column(
        db.DateTime,
        nullable=True
    )

    updated_by = db.Column(
        db.String(100),
        nullable=True
    )

    def __repr__(self):
        return f"<BDCRequest {self.ticket_number}>"