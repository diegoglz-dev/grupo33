from flask import Blueprint
from flask import request
from src.core import services

#from src.core.insts import Institution


api_types_of_services_bp=Blueprint("api_types_of_services", __name__, url_prefix="/api/services-types")

@api_types_of_services_bp.get("/")
def index_types_services():
    types = services.list_types_of_services()  
    if types:   
        types_services = {
            "data": [str(x) for x in types], 
        }
        return types_services, 200
    #En otro caso retorno un mensaje de error
    else:
        return {"error": "Parámetros inválidos"}, 400
    
   