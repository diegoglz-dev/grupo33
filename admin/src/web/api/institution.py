from flask import Blueprint
from flask import request
from src.web.schemas.institution import institution_schema
from src.core import insts
from flask import jsonify


api_institution_bp=Blueprint("institution_api", __name__, url_prefix="/api/institutions")

@api_institution_bp.get("/")
def index_institutions():
    """
    Obtiene una lista paginada de instituciones.

    Recibe parámetros opcionales en la URI para la paginación:
    - page (int): Número de página a recuperar (predeterminado: 1).
    - per_page (int): Número de elementos por página (predeterminado: 1).

    Returns:
        - dict: Un diccionario que contiene información sobre las instituciones paginadas.
            - data (list): Lista de diccionarios representando cada institución.
            - page (int): Número de la página actual.
            - per_page (int): Número de elementos por página.
            - total (int): Número total de instituciones.

    Error Responses:
        - 400 Bad Request: Si los parámetros de paginación son inválidos o no hay instituciones.
    """
    #Recupero los parámetros ingresados en la URI
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=1, type=int)
    #Me quedo con el total de páginas y llamo al método paginate 
    institutions= insts.list_insts_paginate(page=page, per_page=per_page)
    #En caso de que los parametros sean válidos muestro las instituciones
    if institutions is not None and institutions.items:
        institution = {
            "data": [institution_schema.dump(institutions.items)], 
            "page": page,
            "per_page": per_page,
            "total": institutions.total
        }
        return institution, 200
    #En otro caso retorno un mensaje de error
    else:
        return {"error": "Parámetros inválidos"}, 400
    

@api_institution_bp.get("/all", strict_slashes=False)
def get_all_institutions():
    """
    Obtiene una lista de todas las instituciones.

    Returns:
        - dict: Un diccionario que contiene información sobre las instituciones.
            - data (list): Lista de diccionarios representando cada institución.

    Error Responses:
        - 400 Bad Request: Si no hay instituciones.
    """
    #Llamo al método list_insts
    institutions= insts.list_insts()
    #En caso de que haya instituciones las muestro
    if institutions is not None:
        institution = {
            "data": [institution_schema.dump(institutions)], 
        }
        return institution, 200
    #En otro caso retorno un mensaje de error
    else:
        return {"error": "No hay instituciones"}, 400
    

@api_institution_bp.get("/find_inst_by_service/<int:id>")
def find_inst_by_service(id):
    """
    Obtiene el detalle de una institución específica pasandole por parámetro el id del servicio.
    
    """
    inst = insts.find_inst_by_service(id)

    
    if inst:
        institution = {
            "data": institution_schema.dump([inst]),
        }
        return institution, 200
    else:
        return None
    



@api_institution_bp.get("/top_institutions_resolution_time")
def top_institutions_resolution_time():
    """
    Obtiene el top 10 de instituciones con mejor tiempo de resolución.

    Returns:
        - dict: Un diccionario que contiene el top 10 de instituciones con mejor tiempo de resolución.
    """
    # Obtener todas las instituciones
    institutions = insts.list_insts()

    # Crear un diccionario para almacenar el tiempo promedio de resolución de cada institución
    resolution_times = {}

    # Calcular el tiempo promedio de resolución para cada institución
    for institution in institutions:
        average_time = insts.average_resolution_time(institution)
        if average_time is not None:
            resolution_times[institution.name] = average_time

    # Filtrar las instituciones que tienen tiempo promedio de resolución
    valid_institutions = {name: time for name, time in resolution_times.items()}

    # Ordenar las instituciones por tiempo de resolución y tomar el top 10
    sorted_institutions = sorted(
        valid_institutions.items(), key=lambda x: x[1], reverse=True
    )[:10]

    # Crear el resultado como un diccionario
    result = {name: time for name, time in sorted_institutions}

    return jsonify(result), 200
