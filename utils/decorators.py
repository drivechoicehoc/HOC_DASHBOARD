from functools import wraps

from flask import abort

from utils.permissions import has_permission


def permission_required(permission_name):
    """
    Protect a route using a role permission.
    """

    def decorator(view_function):

        @wraps(view_function)
        def wrapped(*args, **kwargs):

            if not has_permission(permission_name):
                abort(403)

            return view_function(*args, **kwargs)

        return wrapped

    return decorator