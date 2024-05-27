from os import environ
from datetime import timedelta


class Config(object):
    SECRET_KEY = environ.get("SECRET_KEY", "secret")
    TESTING = environ.get("TESTING", False)
    SESSION_TYPE = environ.get("SESSION_TYPE", "filesystem")
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY", "secret_key")
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_ACCESS_COOKIE_NAME = "access_token_cookie"
    JWT_TOKEN_HEADER_NAME = "Authorization"
    # Desactivar protección CSRF
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ALGORITHM = "HS256"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)

    # Config Servidor SMTP de tu proveedor de correo
    MAIL_SERVER = environ.get("MAIL_SERVER")
    MAIL_PORT = environ.get("MAIL_PORT", 587)
    MAIL_USERNAME = environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
    MAIL_DEBUG = True
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_SUPPRESS_SEND = False
    # Google OAuth
    GOOGLE_CLIENT_ID = environ.get("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = environ.get("GOOGLE_CLIENT_SECRET")


class ProductionConfig(Config):
    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    DB_PORT = environ.get("DB_PORT")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}"
    )


class DevelopmentConfig(Config):
    DB_USER = environ.get("DB_USER")
    DB_PASS = environ.get("DB_PASS")
    DB_HOST = environ.get("DB_HOST")
    DB_NAME = environ.get("DB_NAME")
    DB_PORT = environ.get("DB_PORT")
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


class TestingConfig(Config):
    TESTING = True


config = {
    "production": ProductionConfig,
    "development": DevelopmentConfig,
    "test": TestingConfig,
}
