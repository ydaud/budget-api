from decimal import Decimal

from app.services import db


class AccountModel(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    balance = db.Column(
        db.Numeric(precision=10, scale=2, asdecimal=True), nullable=False
    )
    type = db.Column(db.Enum("checking", "saving"), nullable=False)

    transactions = db.relationship(
        "TransactionModel", back_populates="account", lazy="dynamic"
    )

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False
    )
    user = db.relationship("UserModel", back_populates="accounts")

    def __init__(self, name: str, balance: float, type: str, user_id: int):
        self.name = name
        self.balance = Decimal(balance)
        self.type = type
        self.user_id = user_id

    def update(self, new_name: str = None, new_type: str = None):
        if new_name:
            self.name = new_name
        if new_type:
            self.type = new_type

    def add_balance(self, amount):
        self.balance += Decimal(amount)

    def __repr__(self):
        return f"<Account: {self.name}, Balance: {self.balance:.2f}>"
