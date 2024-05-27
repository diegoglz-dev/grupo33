from src.web.controllers.user import user_bp
from src.web.controllers.auth import auth_bp
from src.web.controllers.dashboard import dashboard_bp
from src.web.api.institution import api_institution_bp
from src.web.api.profile import api_profile_bp
from src.web.api.auth import api_auth_bp
from src.web.controllers.institution import institution_bp
from src.web.controllers.service import services_bp
from src.web.controllers.configuration import configuration_bp
from src.web.api.type_of_services import api_types_of_services_bp
from src.web.api.service import api_services_bp
from src.web.api.service_request import api_service_requests_bp
from src.web.controllers.service_request import service_requests_bp

def register(app):
    # REGISTRO DE CONTROLADORES
    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(institution_bp)
    app.register_blueprint(services_bp)
    app.register_blueprint(service_requests_bp)
    app.register_blueprint(configuration_bp)
    
    #REGISTRO DE API
    app.register_blueprint(api_institution_bp)
    app.register_blueprint(api_profile_bp)
    app.register_blueprint(api_auth_bp)
    app.register_blueprint(api_types_of_services_bp)   
    app.register_blueprint(api_services_bp)  
    app.register_blueprint(api_service_requests_bp) 
    
