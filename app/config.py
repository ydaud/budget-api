import os

from dotenv import load_dotenv

load_dotenv()

# Find the absolute file path to the top level project directory
basedir = os.path.abspath(os.path.dirname(__name__))


class Config:
    """
    Base configuration class. Contains default configuration settings + configuration settings applicable to all environments.
    """

    # Default settings
    FLASK_ENV = "development"
    FLASK_DEBUG = False
    TESTING = False
    WTF_CSRF_ENABLED = True

    PROPAGATE_EXCEPTIONS = True
    API_TITLE = "Stores REST API"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Settings applicable to all environments
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", default="A worse secret key")
    SECRET_KEY = os.getenv("SECRET_KEY", default="A very terrible secret key.")


class DevelopmentConfig(Config):
    FLASK_DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"


class TestingConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        basedir + "/app/tests", "test.db"
    )


class ProductionConfig(Config):
    FLASK_ENV = "production"
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "PROD_DATABASE_URI", default="sqlite:///prod.db"
    )
