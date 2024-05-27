from flask import render_template
from src.core import configuration


def unauthorized_error(e):
    kwargs = {
        "code_error": "401",
        "error_name": "Unauthorized",
        "error_description": "No tiene los permisos necesarios para acceder",
        "error_message": "¡Lo sentimos!... Si cree que fue un error pongase en contacto con el administrador del sistema. " + configuration.get_configuration().contact
    }

    return render_template("error.html", **kwargs), 401


def forbidden_error(e):
    kwargs = {
        "code_error": "403",
        "error_name": "Forbidden",
        "error_description": "No tiene los permisos necesarios para acceder. Verifique su correo electrónico para activar su cuenta o pongase en contacto con el administrador",
        "error_description": "No tiene los permisos necesarios para acceder",
        "error_message": "Verifique su correo electrónico para activar su cuenta o pongase en contacto con el administrador del sistema. " + configuration.get_configuration().contact
    }

    return render_template("error.html", **kwargs), 403


def not_found_error(e):
    kwargs = {
        "code_error": "404",
        "error_name": "Not Found Error",
        "error_description": "la url a la que quiere acceder no existe",
        "error_message": "¡Lo sentimos!"
    }

    return render_template("error.html", **kwargs), 404


def service_unavailable_maintenance(e):
    config = configuration.get_configuration()
    kwargs = {
        "code_error": "503",
        "error_name": "Service Unavailable",
        "error_description": "Sitio en mantenimiento",
        "error_message": config.maintenance_message
    }

    return render_template("error.html", **kwargs), 503
