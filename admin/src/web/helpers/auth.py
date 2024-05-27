# Flask
from flask import session
from flask import abort
from flask import render_template
from functools import wraps
# Modulo de consultas
from src.core import auth


def is_authenticated(session):
    return session.get("user") is not None


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kargs):
        if not is_authenticated(session):
            return abort(401)
        return f(*args, **kargs)

    return decorated_function


def current_user_auth():
    current_user = session['user']
    return auth.find_user_by_id(current_user.id)


def can_view(permission_name):
    user = current_user_auth()
    return user.has_permission(permission_name)


def permission_required(permission_name):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = session.get("user")

            if current_user:
                if current_user.has_permission(permission_name):
                    return func(*args, **kwargs)
                else:
                    abort(401)
            else:
                return render_template("auth/login.html")

        return wrapper

    return decorator
