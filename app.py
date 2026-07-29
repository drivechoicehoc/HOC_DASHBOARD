from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session
)

from collections import defaultdict
from datetime import datetime
from config import Config
from database.database import db
from utils.permissions import has_permission
from utils.decorators import permission_required
from datetime import datetime

from models.user import User
from models.role import Role
from models.bdc_request import BDCRequest
from seeders.seed_admin import seed_super_admin

from utils.security import verify_password
from models.role_permission import RolePermission

# ============================================
# Blueprints
# ============================================

from routes.bdc_routes import bdc_bp
from routes.employee import employee_bp
from routes.report_routes import report_bp

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)

# ============================================
# Register Blueprints
# ============================================

app.register_blueprint(bdc_bp)
app.register_blueprint(employee_bp)
app.register_blueprint(report_bp)

# ============================================
# Template Context
# ============================================

@app.context_processor
def inject_permissions():
    return {
        "has_permission": has_permission
    }

# ============================================
# Home
# ============================================

@app.route("/")
def home():
    return redirect(url_for("login"))


# ============================================
# Login
# ============================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        print("\n" + "=" * 60)
        print("LOGIN ATTEMPT")
        print(f"Username : {username}")
        print(f"Password : {password}")
        print("=" * 60)

        user = User.query.filter_by(username=username).first()

        if user:

            print("User Found : YES")
            print(f"Employee #: {user.employee_number}")
            print(f"Username   : {user.username}")
            print(f"Active     : {user.active}")
            print(f"Role       : {user.role.name if user.role else 'No Role'}")

            password_ok = verify_password(password, user.password)

            print(f"Password Match : {password_ok}")

            if user.active and password_ok:

                # Update last login
                user.last_login = datetime.now()
                db.session.commit()

                session["user_id"] = user.id
                session["username"] = user.username
                session["role"] = user.role.name

                print("LOGIN SUCCESS")
                print("=" * 60)

                return redirect(url_for("dashboard"))

            print("LOGIN FAILED")

            if not user.active:
                print("Reason: Account is inactive.")

            if not password_ok:
                print("Reason: Password does not match.")

        else:

            print("User Found : NO")

        print("=" * 60)

        return render_template(
            "login.html",
            error="Invalid username or password."
        )

    return render_template("login.html")


# ============================================
# Dashboard
# ============================================

@app.route("/dashboard")
@permission_required("dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect(url_for("login"))

    # Dashboard Statistics

    total_requests = BDCRequest.query.count()

    in_progress_count = BDCRequest.query.filter_by(
        status="In Progress"
    ).count()

    completed_count = BDCRequest.query.filter_by(
        status="Completed"
    ).count()

    cancelled_count = BDCRequest.query.filter_by(
        status="Cancelled"
    ).count()

    # Requests in the BDC Request Queue that reached 1 hour
    one_hour_count = sum(
        1
        for req in BDCRequest.query.filter_by(status="In Progress").all()
        if req.started_at
        and (datetime.now() - req.started_at).total_seconds() >= 3600
    )

    # Latest 5 BDC Requests
    latest_requests = (
        BDCRequest.query
        .order_by(BDCRequest.created_at.desc())
        .limit(5)
        .all()
    )

    # ============================================
    # Top Sales Consultants
    # ============================================

    consultant_stats = defaultdict(
        lambda: {
            "completed_requests": 0,
            "total_seconds": 0
        }
    )

    completed_requests = BDCRequest.query.filter_by(
        status="Completed"
    ).all()

    for request in completed_requests:

        if (
                request.sales_rep
                and request.started_at
                and request.completed_at
        ):
            seconds = (
                    request.completed_at - request.started_at
            ).total_seconds()

            consultant_stats[request.sales_rep]["completed_requests"] += 1
            consultant_stats[request.sales_rep]["total_seconds"] += seconds

    top_sales_consultants = []

    for consultant, stats in consultant_stats.items():
        average_seconds = (
                stats["total_seconds"] /
                stats["completed_requests"]
        )

        top_sales_consultants.append({
            "name": consultant,
            "completed_requests": stats["completed_requests"],
            "average_seconds": average_seconds
        })

    top_sales_consultants.sort(
        key=lambda x: (
            -x["completed_requests"],
            x["average_seconds"]
        )
    )

    top_sales_consultants = top_sales_consultants[:5]

    top_sales_consultants = top_sales_consultants[:5]

    # ============================================
    # Top Sales Managers
    # ============================================

    manager_stats = defaultdict(
        lambda: {
            "completed_requests": 0,
            "total_seconds": 0
        }
    )

    for request in completed_requests:

        if (
                request.sales_manager
                and request.started_at
                and request.completed_at
        ):
            seconds = (
                    request.completed_at - request.started_at
            ).total_seconds()

            manager_stats[request.sales_manager]["completed_requests"] += 1
            manager_stats[request.sales_manager]["total_seconds"] += seconds

    top_sales_managers = []

    for manager, stats in manager_stats.items():
        average_seconds = (
                stats["total_seconds"] /
                stats["completed_requests"]
        )

        top_sales_managers.append({
            "name": manager,
            "completed_requests": stats["completed_requests"],
            "average_seconds": average_seconds
        })

    top_sales_managers.sort(
        key=lambda x: (
            -x["completed_requests"],
            x["average_seconds"]
        )
    )

    top_sales_managers = top_sales_managers[:5]

    return render_template(
        "dashboard.html",
        username=session["username"],
        role=session["role"],
        total_requests=total_requests,
        in_progress_count=in_progress_count,
        completed_count=completed_count,
        cancelled_count=cancelled_count,
        latest_requests=latest_requests,
        top_sales_consultants=top_sales_consultants,
        top_sales_managers=top_sales_managers,
        one_hour_count=one_hour_count,
    )

# ============================================
# Logout
# ============================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ============================================
# Database Initialization
# ============================================

with app.app_context():

    db.create_all()

    roles = [

        "Super Admin",

        # Executive Management
        "Chief Executive Officer (CEO)",
        "President",
        "Vice President",

        # Dealership Management
        "General Manager",
        "Sales Manager",
        "Finance Manager",

        # Business Development Center
        "Sales BDC Manager",
        "Sales BDC Agent",
        "Service BDC Manager",
        "Service BDC Agent",

        # Sales
        "Sales Consultant",
        "Sales Representative",

        # Administration
        "Administrator",
        "Project Manager",

        # Information Technology
        "IT Administrator",
        "System Administrator"

    ]

    for role_name in roles:

        role = Role.query.filter_by(name=role_name).first()

        if not role:

            db.session.add(
                Role(
                    name=role_name,
                    description=f"{role_name} Role"
                )
            )

    db.session.commit()

    seed_super_admin()
    for role in Role.query.all():

        if not RolePermission.query.filter_by(role_id=role.id).first():
            db.session.add(
                RolePermission(
                    role_id=role.id
                )
            )

    db.session.commit()

# ============================================
# Error Handlers
# ============================================

@app.errorhandler(403)
def forbidden(error):
    return render_template(
        "errors/403.html"
    ), 403

# ============================================
# Run Application
# ============================================

if __name__ == "__main__":
    app.run(debug=True)
