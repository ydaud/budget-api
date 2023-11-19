from datetime import datetime
from decimal import Decimal

from app.services import db


class BudgetModel(db.Model):
    __tablename__ = "budgets"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    available = db.Column(
        db.Numeric(precision=10, scale=2, asdecimal=True), nullable=False
    )

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False
    )
    user = db.relationship("UserModel", back_populates="budgets")

    months = db.relationship("MonthModel", back_populates="budget", lazy="dynamic")

    def __init__(self, name: str, user_id: int):
        self.name = name
        self.available = Decimal(0.00)
        self.user_id = user_id

    def update_available(self, added_available: float):
        self.available += Decimal(added_available)


class MonthModel(db.Model):
    __tablename__ = "months"

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.DateTime)

    budget_id = db.Column(
        db.Integer, db.ForeignKey("budgets.id"), unique=False, nullable=False
    )
    budget = db.relationship("BudgetModel", back_populates="months")

    entries = db.relationship("EntryModel", back_populates="month", lazy="dynamic")

    def __init__(self, month: datetime, budget_id: int):
        self.month = month
        self.budget_id = budget_id


class EntryModel(db.Model):
    __tablename__ = "entry"

    id = db.Column(db.Integer, primary_key=True)
    assigned = db.Column(
        db.Numeric(precision=10, scale=2, asdecimal=True), nullable=False
    )
    activity = db.Column(
        db.Numeric(precision=10, scale=2, asdecimal=True), nullable=False
    )
    available = db.Column(
        db.Numeric(precision=10, scale=2, asdecimal=True), nullable=False
    )

    month_id = db.Column(
        db.Integer, db.ForeignKey("months.id"), unique=False, nullable=False
    )
    month = db.relationship("MonthModel", back_populates="entries")

    category_id = db.Column(
        db.Integer, db.ForeignKey("category.id"), unique=False, nullable=False
    )
    category = db.relationship("CategoryModel", back_populates="entries")

    def __init__(
        self, month_id: int, category_id: int, assigned: float, available: float
    ):
        self.assigned = Decimal(assigned)
        self.activity = Decimal(0.00)
        self.available = Decimal(available)
        self.month_id = month_id
        self.category_id = category_id

    def update_assigned(self, new_assigned: float):
        self.assigned = Decimal(new_assigned)
        self.available = self.assigned - self.activity
