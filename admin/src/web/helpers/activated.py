from functools import wraps
from flask import session
from flask import abort

from src.core.auth import find_user_by_email


def is_activated(f):
    @wraps(f)
    def decorated_function(*args, **kargs):
        user = find_user_by_email(session['email'])
        if not user.active:
            return abort(403)

        return f(*args, **kargs)

    return decorated_function
