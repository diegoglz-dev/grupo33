from flask import Blueprint
from flask import request
from flask import jsonify
from flask import url_for
from src.core import auth
# Importa la configuración de OAuth
from src.web.oauth_config import oauth
# Importa las funciones para crear y verificar tokens
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from flask_jwt_extended import unset_jwt_cookies, jwt_required
from flask_jwt_extended import get_jwt_identity


api_auth_bp = Blueprint("auth_api", __name__, url_prefix="/api/auth")


@api_auth_bp.post('/login')
def login():
    """
    Autentica a un usuario usando JWT.
    Recibe datos de autenticación en formato JSON desde el cuerpo de la solicitud.
    returns:
        dict: Un diccionario que contiene un token JWT si la autenticación es exitosa.
              En caso contrario, devuelve un diccionario con un mensaje de error y un código de estado 401.
    """
    data_auth = request.get_json()
    user = auth.check_user(data_auth["email"], data_auth["password"])
    if user:
        access_token = create_access_token(identity=user.id)
        response = jsonify({"token": access_token, "user_first_name": user.first_name,
                           "user_last_name": user.last_name, "user_email": user.email})
        set_access_cookies(response, access_token)
        return response, 201
    else:
        return {"error": "Usuario, email o contraseña ingresados son inválidos"}, 401


@api_auth_bp.post('/register')
def register():
    data_auth = request.get_json()

    user = auth.find_user_by_email(data_auth["email"])
    if user:
        return {"error": "El email ya existe"}, 401
    user = auth.find_user_by_username(data_auth["username"])
    if user:
        return {"error": "El nombre de usuario ya existe"}, 401
    if data_auth["password"] != data_auth["password_confirmation"]:
        return {"error": "Las contraseñas no coinciden"}, 401
    user = auth.create_user(
        first_name=data_auth["first_name"],
        last_name=data_auth["last_name"],
        username=data_auth["username"],
        email=data_auth["email"],
        password=data_auth["password"],
        active=True,
    )
    if user:
        access_token = create_access_token(identity=user.id)
        response = jsonify({"token": access_token, "user_first_name": user.first_name,
                           "user_last_name": user.last_name, "user_email": user.email})
        set_access_cookies(response, access_token)
        return response, 201
    else:
        return {"error": "Parámetros inválidos"}, 401


@api_auth_bp.get('/login-google')
def login_google():
    redirect_uri = url_for('auth_api.auth_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@api_auth_bp.get('/login-google/callback')
def auth_google():
    token = oauth.google.authorize_access_token()
    email_google = token['userinfo']['email']
    user = auth.find_user_by_email(email_google)
    if user is None:
        # Separar el nombre completo en nombre y apellido
        full_name = token['userinfo']['name']
        if full_name:
            first_name, *last_name_parts = full_name.split()
            last_name = ' '.join(last_name_parts)

        user = auth.create_user(
            first_name=first_name,
            last_name=last_name,
            username=auth.generate_unique_username(first_name, last_name),
            email=email_google,
            password="password",
            active=True,
        )
    access_token = create_access_token(identity=user.id)
    response = jsonify({"token": access_token})
    # Seteo la cookie
    set_access_cookies(response, access_token)
    return response, 201


@api_auth_bp.get('/logout-google')
@jwt_required()
def logout_google():
    response = jsonify()
    unset_jwt_cookies(response)
    return response, 200
