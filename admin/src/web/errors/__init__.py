from src.web.errors import error


def register(app):
    # REGISTRO DE ERRORES
    app.register_error_handler(401, error.unauthorized_error)
    app.register_error_handler(403, error.forbidden_error)
    app.register_error_handler(404, error.not_found_error)
    app.register_error_handler(503, error.service_unavailable_maintenance)
