from flask import session
from models.user import User


def has_permission(permission_name):
    """
    Check if the currently logged-in user has the specified permission.

    Super Admin always has full access.
    """

    # User is not logged in
    if "user_id" not in session:
        return False

    # Get the current user
    user = User.query.get(session["user_id"])

    # User or role does not exist
    if not user or not user.role:
        return False

    # ----------------------------------------------------------
    # Super Admin Override
    # ----------------------------------------------------------
    # Super Admin always has access to every page and action.
    # This prevents accidentally locking yourself out of the
    # administration panel.
    # ----------------------------------------------------------
    if user.role.name == "Super Admin":
        return True

    # Role has no permissions assigned
    if not user.role.permissions:
        return False

    # Check the requested permission
    return getattr(user.role.permissions, permission_name, False)