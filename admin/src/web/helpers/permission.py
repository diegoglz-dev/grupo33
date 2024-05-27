# Flask
from flask import session
from flask import abort
from flask import render_template
from functools import wraps
# Modulo de consultas
from src.core import auth

def permission_required(permission_name):
    def decorator(func):
        @wraps(func)
        def wrapper(id_inst,*args, **kwargs):
            user = session.get("user")
            print("-------------------------------")
            print(user)
            print(id_inst)
            print("-------------------------------")
            c = auth.user_rol_inst(user.id, id_inst)

            if c and c.has_permission(permission_name):
                return func(id_inst,*args, **kwargs)
            else:
                abort(401)

        return wrapper

    return decorator
