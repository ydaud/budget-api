import datetime
import logging

from flask.views import MethodView
from flask_jwt_extended import create_access_token, get_jwt, jwt_required
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError

from app import db
from app.models import UserModel
from app.schemas import UserSchema
from app.services.jwt_service import BLOCKLIST

LOG = logging.getLogger(__name__)

blp = Blueprint("Users", "users", description="Operations on users")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        email = user_data["email"]
        password = user_data["password"]
        user = UserModel(email=email, password=password)

        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            LOG.error(f"User {email} already exists")
            db.session.rollback()
            abort(409, message="A user with that email already exists.")

        return {"message": "User created successfully."}, 201


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter_by(email=user_data["email"]).first()

        if user and user.is_password_correct(user_data["password"]):
            expires = datetime.timedelta(hours=2)
            access_token = create_access_token(identity=user.id, expires_delta=expires)
            return {"email": user.email, "access_token": access_token}, 200

        LOG.error(f"User doesn't exist")
        abort(401, message="Invalid credentials.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


@blp.route("/user/<int:user_id>")
class User(MethodView):
    """
    This resource can be useful when testing our Flask app.
    We may not want to expose it to public users, but for the
    sake of demonstration in this course, it can be useful
    when we are manipulating data regarding the users.
    """

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
