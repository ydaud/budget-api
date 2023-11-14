import os

from dotenv import load_dotenv
from flask import Flask, request

from app.services import api, cors, db, jwt, migrate

# loading environment variables
load_dotenv()


def create_app():
    app = Flask(__name__)

    # Configure the flask app instance
    CONFIG_TYPE = os.getenv("CONFIG_TYPE", default="app.config.DevelopmentConfig")
    app.config.from_object(CONFIG_TYPE)

    # Initialize flask extension objects
    initialize_extensions(app)

    # Register blueprints
    register_blueprints(app)

    # Configure logging
    configure_logging(app)

    # Register error handlers
    register_error_handlers(app)

    return app


def register_blueprints(app):
    from app.controllers import AccountBlueprint, TransactionBlueprint, UserBlueprint

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(AccountBlueprint)
    app.register_blueprint(TransactionBlueprint)


def initialize_extensions(app):
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    cors.init_app(app)

    from app.models import AccountModel, TransactionModel, UserModel


def configure_logging(app):
    import logging
    from logging.handlers import RotatingFileHandler

    from flask.logging import default_handler

    app.logger.removeHandler(default_handler)

    file_formatter = logging.Formatter(
        "%(asctime)s %(levelname)s: %(message)s [in %(filename)s: %(lineno)d]"
    )

    file_handler = RotatingFileHandler("logs/app.log", maxBytes=16384, backupCount=20)
    file_handler.setFormatter(file_formatter)

    app.logger.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)


def register_error_handlers(app):
    pass
