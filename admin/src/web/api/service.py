from flask import Blueprint
from src.core import services
from flask import request
from src.web.schemas.service import services_schema, service_schema
from src.core import configuration
import json


api_services_bp=Blueprint("api_services", __name__, url_prefix="/api/services")

@api_services_bp.get("/<int:id>")
def show_service_detail(id):
    """
    Obtiene el detalle de un servicio específico. 

    """
    # Parsear los parámetros de la URI
    serv= services.find_service_by_id(id)
    if serv:
        return service_schema.dump(serv), 200
    #En otro caso retorno un mensaje de error    
    return {"error": "Parámetros inválidos"}, 400
    
   

@api_services_bp.get("/search")
def index_services():
    """
    Busca servicios basados en parámetros proporcionados en la URI.

    Parámetros de la URI:
        - q (str): Término de búsqueda opcional para el nombre del servicio.
        - type (str): Tipo de servicio opcional.
        - page (int): Número de página a recuperar (predeterminado: 1).
        - per_page (int): Número de elementos por página (predeterminado: valor configurado).

    Returns:
        - dict: Un diccionario que contiene los servicios coincidentes con los parámetros de búsqueda.

    Error Responses:
        - 400 Bad Request: Si los parámetros de la solicitud son inválidos o insuficientes.
    """
    # Parsear los parámetros de la URI
    q = request.args.get("q", None)
    type = request.args.get("type", None)
    page = request.args.get("page", default=1, type=int)
    per_page = request.args.get("per_page", default=configuration.get_configuration().per_page, type=int)

    if q:
        servs= services.list_service_by_name_type(q, type, page, per_page)
        if servs:
            servs_data = {
            "data": [services_schema.dump(servs.items)], 
            "page": page,
            "per_page": per_page,
            "total": servs.total
            }
            return servs_data, 200
    #En otro caso retorno un mensaje de error    
    return {"error": "Parámetros inválidos"}, 400


@api_services_bp.get("/most_requested")
def sservices_most_requested():
    """
    Obtiene los servicios más solicitados.

    Returns:
        - dict: Un diccionario que contiene los servicios más solicitados.

    Error Responses:
        - 400 Bad Request: Si los parámetros de la solicitud son inválidos o insuficientes.
    """
    servs = services.services_most_requested()
    print(servs)

    # Serializar manualmente el objeto ServiceType
    for service in servs:
        service['type_of_service'] = service['type_of_service'].value
        print(service['type_of_service'])

    # Convertir la lista de diccionarios a una cadena JSON formateada
    formatted_json = json.dumps(servs, indent=2, ensure_ascii=False, default=str)
    print(formatted_json)
    
    return formatted_json, 200





    
   