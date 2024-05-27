from flask import Flask
from flask import render_template
from flask_session import Session
from src.web.config import config
from src.core import database
from src.web import commands
from src.web import routes
from src.web import errors
from src.web import mail
from src.web.helpers import auth
# Importa la configuración de OAuth
from src.web.oauth_config import oauth
from flask_jwt_extended import JWTManager
from flask_cors import CORS

session = Session()
jwt = JWTManager()


def create_app(env="development", static_folder="../../static"):
    app = Flask(__name__, static_folder=static_folder)

    # REGISTRO CONFIG. DE ENTORNO
    app.config.from_object(config[env])
    # CORS(app, resources={r"/api/*": {"origins": "*"}})
    # print(app.config)

    CORS(app, supports_credentials=True)
    # AGREGA LA CONFIGURACIÓN DE OAUTH
    oauth.init_app(app)
    # EXTENDS
    database.init_app(app)
    session.init_app(app)
    jwt.init_app(app)
    # REGISTRO DE MAIL
    mail.init_app(app)
    # AGREGA COMANDOS A FLASK
    commands.register(app)
    # REGISTRO DE CONTROLADORES
    routes.register(app)
    # REGISTRO DE METODOS EN JINJA
    app.jinja_env.globals.update(is_authenticated=auth.is_authenticated)
    app.jinja_env.globals.update(can_view=auth.can_view)
    # REGISTRO DE ERRORES
    errors.register(app)

    @app.route("/")
    def home():
        return render_template("home.html")

    return app
