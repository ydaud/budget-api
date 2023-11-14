from datetime import datetime
from decimal import Decimal

from app.services import db


class TransactionModel(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    payee = db.Column(db.String(150))
    inflow = db.Column(db.Boolean)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    raw_value = db.Column(
        db.Numeric(precision=10, scale=2, asdecimal=True), nullable=False
    )

    account_id = db.Column(
        db.Integer, db.ForeignKey("accounts.id"), unique=False, nullable=False
    )
    account = db.relationship("AccountModel", back_populates="transactions")

    def __init__(
        self, date: datetime, payee: str, amount: float, inflow: bool, account_id: int
    ):
        self.date = date
        self.payee = payee

        if amount < 0:
            inflow = not inflow
            amount = amount * -1

        self.inflow = Decimal(inflow)
        self.amount = amount
        self.raw_value = Decimal(amount) if inflow else Decimal(amount * -1)
        self.account_id = account_id

    def __repr__(self):
        return f"<Transaction: {self.payee} {self.raw_value:.2f}>"
