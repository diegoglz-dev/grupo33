from functools import wraps
from flask import abort
from flask import session
from src.core import configuration
from src.core import auth


def is_in_maintenance_mode(f):
    @wraps(f)
    def decorated_function(*args, **kargs):
        user_session = session['user']
        is_user_super_admin = auth.user_has_role(
            auth.find_user_by_id(user_session.id), 'Super-Administrador')

        enabled_site = configuration.get_configuration().enabled_site
        if enabled_site:
            return f(*args, **kargs)
        if is_user_super_admin:
            return f(*args, **kargs)
        return abort(503)

    return decorated_function
