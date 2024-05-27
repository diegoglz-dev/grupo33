from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt_identity
from flask import Blueprint
from src.web.schemas.profile import profile_schema
from src.core import auth



api_profile_bp=Blueprint("profile_api", __name__, url_prefix="/api/me/profile")
@api_profile_bp.get("/")
@jwt_required()
def profile_jwt():
    """
    Obtiene el perfil del usuario actual autenticado.

    Utiliza el token JWT proporcionado en la solicitud para identificar al usuario actual.

    Returns:
        - str: Representación JSON del perfil del usuario.

    Error Responses:
        - 401 Unauthorized: Si el token JWT no es válido o no está presente.
        - 400 Bad Request: Si hay parámetros inválidos o el usuario no se encuentra.
    """
    #Recupero al usuario a partir del username
    current_user = get_jwt_identity()
    user = auth.find_user_by_id(current_user)
    if user:
        return profile_schema.dumps(user), 200
    #En otro caso retorno un json de error
    else:
        return {"error": "Parámetros inválidos"}, 400

