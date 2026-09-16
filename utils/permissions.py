from flask import session, g
from models.user import User


def has_permission(permission_name):
    """
    Check if the currently logged-in user has the specified permission.

    The current user's role and permissions are loaded once per request
    and reused for subsequent permission checks.
    """

    # User is not logged in
    if "user_id" not in session:
        return False

    # Load the current user only once per request
    if not hasattr(g, "current_user"):
        g.current_user = User.query.get(session["user_id"])

    user = g.current_user

    # User or role does not exist
    if not user or not user.role:
        return False

    # Super Admin always has access
    if user.role.name == "Super Admin":
        return True

    # Role has no permissions assigned
    if not user.role.permissions:
        return False

    # Check the requested permission
    return getattr(user.role.permissions, permission_name, False)
