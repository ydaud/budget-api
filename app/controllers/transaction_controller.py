import logging

from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort

from app import db
from app.models import AccountModel, TransactionModel
from app.schemas import TransactionSchema

LOG = logging.getLogger(__name__)

blp = Blueprint(
    "Transactions", "transactions", description="Operations on transactions"
)


@blp.route("/accounts/<string:account_id>/transactions")
class Transaction(MethodView):
    @jwt_required()
    @blp.response(200, TransactionSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        transactions = TransactionModel.query.filter_by(user_id=user_id).all()
        return transactions

    @jwt_required()
    @blp.arguments(TransactionSchema)
    @blp.response(201, TransactionSchema)
    def post(self, transaction, account_id):
        user_id = get_jwt_identity()

        account = AccountModel.query.filter_by(user_id=user_id, id=account_id).first()
        if not account:
            LOG.error(f"Account {account_id} does not exist")
            abort(409, message="An account with that id does not exist")

        payee = transaction["payee"]
        date = transaction["date"]
        inflow = transaction["inflow"]
        amount = transaction["amount"]
        transaction = TransactionModel(
            date=date, payee=payee, amount=amount, inflow=inflow, account_id=account_id
        )

        account.add_balance(transaction.raw_value)

        db.session.add(account)
        db.session.add(transaction)
        db.session.commit()

        return transaction


@blp.route("/accounts/<string:account_id>/transactions/<string:transaction_id>")
class Transaction(MethodView):
    @jwt_required()
    @blp.response(200, TransactionSchema)
    def get(self, transaction_id):
        user_id = get_jwt_identity()
        transactions = TransactionModel.query.filter_by(
            user_id=user_id, transaction_id=transaction_id
        ).all()
        return transactions
