import logging

from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort

from app import db
from app.models import AccountModel
from app.schemas import AccountSchema, AccountUpdateSchema

LOG = logging.getLogger(__name__)

blp = Blueprint("Accounts", "accounts", description="Operations on accounts")


@blp.route("/accounts")
class AllAccounts(MethodView):
    @jwt_required()
    @blp.response(200, AccountSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        accounts = AccountModel.query.filter_by(user_id=user_id).all()
        return accounts

    @jwt_required()
    @blp.arguments(AccountSchema)
    @blp.response(201, AccountSchema)
    def post(self, account_data):
        name = account_data["name"]
        balance = account_data["balance"]
        type = account_data["type"]
        user_id = get_jwt_identity()

        query_name = AccountModel.query.filter_by(user_id=user_id, name=name).first()
        if query_name:
            LOG.error(f"Account {name} already exists")
            abort(409, message="An account with that name already exists")

        account = AccountModel(name, balance, type, user_id)

        db.session.add(account)
        db.session.commit()

        return account


@blp.route("/accounts/<string:account_id>")
class Account(MethodView):
    @jwt_required()
    @blp.response(200, AccountSchema)
    def get(self, account_id):
        user_id = get_jwt_identity()
        account = AccountModel.query.filter_by(user_id=user_id, id=account_id).first()

        if not account:
            LOG.error(f"Account {id} does not exist")
            abort(404, message="An account with that id does not exist.")

        return account

    @jwt_required()
    @blp.arguments(AccountUpdateSchema)
    @blp.response(200, AccountSchema)
    def put(self, new_account_data, account_id):
        user_id = get_jwt_identity()
        account = AccountModel.query.filter_by(user_id=user_id, id=account_id).first()

        if not account:
            LOG.error(f"Account {id} does not exist")
            abort(404, message="An account with that id does not exist.")

        name = new_account_data.get("name")
        if name:
            query_name = AccountModel.query.filter_by(
                user_id=user_id, name=name
            ).first()
            if query_name:
                LOG.error(f"Account {name} already exists")
                abort(409, message="An account with that name already exists")

        account.update(
            new_name=new_account_data.get("name"), new_type=new_account_data.get("type")
        )

        db.session.add(account)
        db.session.commit()

        return account
