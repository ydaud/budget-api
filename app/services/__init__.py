from flask_cors import CORS
from flask_migrate import Migrate
from flask_smorest import Api

from app.services.db_service import db
from app.services.jwt_service import jwt

migrate = Migrate()
api = Api()
cors = CORS()
