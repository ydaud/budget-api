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


@blp.route("/transactions")
class Transaction(MethodView):
    @jwt_required()
    @blp.response(200, TransactionSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        transactions = (
            TransactionModel.query.join(AccountModel)
            .filter(AccountModel.user_id == user_id)
            .all()
        )
        return transactions

    @jwt_required()
    @blp.arguments(TransactionSchema)
    @blp.response(201, TransactionSchema)
    def post(self, transaction):
        user_id = get_jwt_identity()
        account_id = transaction["account_id"]

        account = AccountModel.query.filter_by(
            user_id=user_id, id=account_id
        ).first_or_404()

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


@blp.route("/transactions/<string:transaction_id>")
class Transaction(MethodView):
    @jwt_required()
    @blp.response(200, TransactionSchema)
    def get(self, transaction_id):
        user_id = get_jwt_identity()
        transaction = TransactionModel.query.filter_by(id=transaction_id).first_or_404(
            description="transaction does not exist"
        )
        return transaction
