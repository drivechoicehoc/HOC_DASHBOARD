from datetime import datetime, timezone

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
)

from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from database.database import db

from models.user import User
from models.role import Role
from models.bdc_request import BDCRequest
from utils.ticket import generate_ticket
from utils.decorators import permission_required

bdc_bp = Blueprint("bdc", __name__)


# ==========================================================
# Add BDC Request
# ==========================================================

@bdc_bp.route("/bdc/add", methods=["GET", "POST"])
@permission_required("new_bdc_request")
def add_request():

    if "user_id" not in session:
        return redirect(url_for("login"))

    # ------------------------------------------
    # Sales Consultants
    # ------------------------------------------

    sales_reps = (
        User.query
        .options(joinedload(User.role))
        .join(Role)
        .filter(
            Role.name == "Sales Consultant"
        )
        .order_by(User.first_name)
        .all()
    )
    # ------------------------------------------
    # Sales Managers
    # ------------------------------------------

    sales_managers = (
        User.query
        .join(Role)
        .filter(
            Role.name.in_([
                "Sales Manager",
                "General Manager"
            ])
        )
        .order_by(User.first_name)
        .all()
    )

    if request.method == "POST":

        now = datetime.now(timezone.utc)

        full_name = request.form.get("full_name", "").strip()

        name_parts = full_name.split()

        first_name = name_parts[0] if len(name_parts) >= 1 else ""
        last_name = name_parts[-1] if len(name_parts) >= 2 else ""
        middle_name = " ".join(name_parts[1:-1]) if len(name_parts) >= 3 else ""

        new_request = BDCRequest(

            # Ticket Information
            ticket_number=generate_ticket(),
            created_at=now,
            started_at=now,
            completed_at=None,

            bdc_agent=session["username"],

            # Request Type
            request_type=request.form.get("request_type"),
            other_request_type=request.form.get("other_request_type"),

            # Customer
            first_name=first_name,
            middle_name=middle_name,
            last_name=last_name,

            phone=request.form.get("phone"),
            email=request.form.get("email"),

            # Assignment
            sales_rep=request.form.get("sales_rep"),
            sales_manager=request.form.get("sales_manager"),

            # Vehicle
            vehicle_year=request.form.get("vehicle_year"),
            vehicle_make=request.form.get("vehicle_make"),
            vehicle_model=request.form.get("vehicle_model"),
            vehicle_trim=request.form.get("vehicle_trim"),

            stock_number=request.form.get("stock_number"),
            vin=request.form.get("vin"),

            # BDC Internal Notes
            bdc_internal_notes=request.form.get("bdc_internal_notes"),

            # Resolution
            resolution="",

            # Status
            status="In Progress",

            updated_at=None,
            updated_by=None
        )

        db.session.add(new_request)
        db.session.commit()

        return redirect(url_for("bdc.list_requests"))

    return render_template(
        "bdc_requests/add.html",
        ticket_number=generate_ticket(),
        created_at=datetime.now().strftime("%m/%d/%Y %I:%M %p"),
        bdc_agent=session["username"],
        sales_reps=sales_reps,
        sales_managers=sales_managers
    )
# ==========================================================
# List Requests
# ==========================================================

@bdc_bp.route("/bdc/list")
@permission_required("bdc_request_queue")
def list_requests():

    if "user_id" not in session:
        return redirect(url_for("login"))

    # ------------------------------------------
    # Search / Filter Values
    # ------------------------------------------

    search = request.args.get("search", "").strip()

    request_type = request.args.get("request_type", "").strip()

    sales_rep = request.args.get("sales_rep", "").strip()

    status = request.args.get("status", "").strip()

    # ------------------------------------------
    # Base Query
    # ------------------------------------------

    query = BDCRequest.query

    # ------------------------------------------
    # Search
    # ------------------------------------------

    if search:

        query = query.filter(

            or_(

                BDCRequest.ticket_number.ilike(f"%{search}%"),

                BDCRequest.first_name.ilike(f"%{search}%"),

                BDCRequest.middle_name.ilike(f"%{search}%"),

                BDCRequest.last_name.ilike(f"%{search}%"),

                BDCRequest.phone.ilike(f"%{search}%")

            )

        )

    # ------------------------------------------
    # Filters
    # ------------------------------------------

    if request_type:

        query = query.filter(
            BDCRequest.request_type == request_type
        )

    if sales_rep:

        query = query.filter(
            BDCRequest.sales_rep == sales_rep
        )

    if status:

        query = query.filter(
            BDCRequest.status == status
        )

    # ------------------------------------------
    # Results
    # ------------------------------------------

    requests = (

        query

        .order_by(BDCRequest.id.desc())

        .all()

    )

    # ------------------------------------------
    # Dropdown Lists
    # ------------------------------------------

    request_types = (

        db.session.query(BDCRequest.request_type)

        .distinct()

        .order_by(BDCRequest.request_type)

        .all()

    )

    sales_reps = (

        db.session.query(BDCRequest.sales_rep)

        .filter(BDCRequest.sales_rep.isnot(None))

        .distinct()

        .order_by(BDCRequest.sales_rep)

        .all()

    )


    statuses = (

        db.session.query(BDCRequest.status)

        .distinct()

        .order_by(BDCRequest.status)

        .all()

    )

    return render_template(

        "bdc_requests/list.html",

        requests=requests,

        search=search,

        selected_request_type=request_type,

        selected_sales_rep=sales_rep,

        selected_status=status,

        request_types=request_types,

        sales_reps=sales_reps,

        statuses=statuses

    )

    # ==========================================================
    # View Request
    # ==========================================================

@bdc_bp.route("/bdc/view/<int:id>")
def view_request(id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    bdc_request = BDCRequest.query.get_or_404(id)

    return render_template(
        "bdc_requests/view.html",
        request=bdc_request
    )
# ==========================================================
# Edit Request
# ==========================================================

@bdc_bp.route("/bdc/edit/<int:id>", methods=["GET", "POST"])
def edit_request(id):

    if "user_id" not in session:
        return redirect(url_for("login"))

    bdc_request = BDCRequest.query.get_or_404(id)

    sales_reps = (
        User.query
        .join(Role)
        .filter(
            Role.name.in_([
                "Sales Consultant",
                "Sales Representative"
            ])
        )
        .order_by(User.first_name)
        .all()
    )

    sales_managers = (
        User.query
        .join(Role)
        .filter(
            Role.name.in_([
                "Sales Manager",
                "General Manager"
            ])
        )
        .order_by(User.first_name)
        .all()
    )

    if request.method == "POST":

        # Request Type
        bdc_request.request_type = request.form.get("request_type")
        bdc_request.other_request_type = request.form.get("other_request_type")

        # Customer
        bdc_request.first_name = request.form.get("first_name")
        bdc_request.middle_name = request.form.get("middle_name")
        bdc_request.last_name = request.form.get("last_name")

        bdc_request.address = request.form.get("address")
        bdc_request.phone = request.form.get("phone")
        bdc_request.email = request.form.get("email")

        # Assignment
        bdc_request.sales_rep = request.form.get("sales_rep")
        bdc_request.sales_manager = request.form.get("sales_manager")

        # Vehicle
        bdc_request.vehicle_year = request.form.get("vehicle_year")
        bdc_request.vehicle_make = request.form.get("vehicle_make")
        bdc_request.vehicle_model = request.form.get("vehicle_model")
        bdc_request.vehicle_trim = request.form.get("vehicle_trim")
        bdc_request.stock_number = request.form.get("stock_number")
        bdc_request.vin = request.form.get("vin")

        # Resolution
        bdc_request.resolution = request.form.get("resolution")

        # Status
        new_status = request.form.get("status")
        bdc_request.status = new_status
        if new_status == "In Progress" and not bdc_request.started_at:
            bdc_request.started_at = datetime.now(timezone.utc)

        if new_status == "Completed" and not bdc_request.completed_at:
            bdc_request.completed_at = datetime.now(timezone.utc)

        bdc_request.updated_at = datetime.now(timezone.utc)
        bdc_request.updated_by = session["username"]

        db.session.commit()

        return redirect(url_for("bdc.view_request", id=bdc_request.id))

    return render_template(
        "bdc_requests/edit.html",
        request=bdc_request,
        sales_reps=sales_reps,
        sales_managers=sales_managers
    )
# ==========================================================
# Delete Request
# ==========================================================

@bdc_bp.route("/bdc/delete/<int:id>", methods=["POST"])
@permission_required("delete_bdc_request")
def delete_request(id):

    bdc_request = BDCRequest.query.get_or_404(id)

    db.session.delete(bdc_request)
    db.session.commit()

    return redirect(url_for("bdc.list_requests"))