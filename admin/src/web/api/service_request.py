from flask import Blueprint
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask import request
from src.web.schemas.service_request import service_requests_schema, service_request_schema
from src.core import configuration
from src.core import auth, service_requests


api_service_requests_bp = Blueprint(
    "api_service_requests", __name__, url_prefix="/api/me")


@api_service_requests_bp.post("/requests/")
@jwt_required()
def create_service_request():
    """
    Crea un servicio asociado al usuario autenticado. 
    """

    # Recupero al usuario a partir del username
    current_user = get_jwt_identity()
    user = auth.find_user_by_id(current_user)
    # Me quedo con los datos ingresados en el body
    data = request.get_json()

    # Validación de datos
    # if not data or "title" not in data or "description" not in data:

    # Creo la solicitud
    if user:
        serv = service_requests.create_service_request(
            title=data["title"],
            description=data["description"],
            user_id=user.id,
            service_id=int(data["service_id"])
        )
        service_requests.create_event_service_request(
            service_request_id=serv.id,
            observation="",
            state_request_id=1,
        )

        return {"title": data["title"], "description": data["description"]}, 201
    return {"error": "Datos de entrada inválidos"}, 400


@api_service_requests_bp.get("/requests/")
@jwt_required()
def index_service_requests_me():
    """
    Obtiene el listado de solicitudes realizadas por el usuario autenticado.
    """
   # Recupero los parámetros ingresados en la URI
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get(
        "per_page", default=configuration.get_configuration().per_page, type=int)
    sort = request.args.get("sort", None)
    order = request.args.get("order", default="desc", type=str)
    # Recupero al usuario a partir del username
    current_user = get_jwt_identity()
    user = auth.find_user_by_id(current_user)
    # Llamo al método get requests
    serv_requests = user.get_request_paginate(
        sort=sort, order=order, page=page, per_page=per_page)

    # En caso de que los parametros sean válidos muestro las instituciones
    if serv_requests:
        requests = {
            "data": [service_requests_schema.dump(serv_requests.items)],
            "page": page,
            "per_page": per_page,
            "total": serv_requests.total
        }
        return requests, 200
    # En otro caso retorno un mensaje de error
    else:
        return {"error": "Parámetros inválidos"}, 400


@api_service_requests_bp.get("/requests/<int:id>")
@jwt_required()
def show_service_detail(id):
    """
    Obtiene el detalle de un servicio específico. 

    """
    # Recupero al usuario a partir del username
    current_user = get_jwt_identity()
    user = auth.find_user_by_id(current_user)
    # Llamo al método get requests
    serv_request = user.get_request_id(id=id)
    if serv_request:
        return service_request_schema.dump(serv_request), 200
    # En otro caso retorno un mensaje de error
    return {"error": "Parámetros inválidos"}, 400


@api_service_requests_bp.post("/requests/<int:id>/notes/")
@jwt_required()
def create_service_request_note(id):
    """
    Crea una nota. 

    id: es el id de la solicitud de servicio
    """
    # Me quedo con los datos ingresados en el body
    data = request.get_json()

    # Validación de datos
    if not data or "text_note" not in data:
        return {"error": "Datos de entrada inválidos"}, 400

    note = data["text_note"]

    # Recupero al usuario a partir del username
    current_user = get_jwt_identity()
    user = auth.find_user_by_id(current_user)

    # Llamo al método get requests
    reque = user.get_request_id(id=id)

    # Para que no se guarde una nota vacía
    if reque and note:
        # Guardo la nota y la retorno
        service_requests.create_note_request(
            service_request_id=reque.id,
            note=note
        )
        return {"text_note": note}, 201

    # En otro caso retorno un mensaje de error
    return {"error": "Parámetros inválidos"}, 400


@api_service_requests_bp.get("/requests/<int:id>/notes/")
@jwt_required()
def show_service_request_note(id):
    """
     Retorna las notas de una solicitud.
    """
    serv = service_requests.find_service_request_by_id(id)
    return serv.get_notes_as_json(), 200


@api_service_requests_bp.get("/requests/solicitudes_por_estado")
def solicitudes_por_estado():
    """
    Obtiene la cantidad de solicitudes realizadas agrupadas por estado.

    Returns:
        - dict: Un diccionario que contiene la cantidad de solicitudes por estado.

    Error Responses:
        - 400 Bad Request: Si los parámetros de la solicitud son inválidos o insuficientes.
    """
    solicitudes_estado = service_requests.solicitudes_por_estado()
    if solicitudes_estado:
        return solicitudes_estado, 200

    return {"error": "Parámetros inválidos"}, 400
