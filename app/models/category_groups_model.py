from decimal import Decimal

from app.services import db


class CategoryGroupModel(db.Model):
    __tablename__ = "category_groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    assigned = db.Column(
        db.Numeric(precision=10, scale=2, asdecimal=True), nullable=False
    )
    activity = db.Column(
        db.Numeric(precision=10, scale=2, asdecimal=True), nullable=False
    )

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False
    )
    user = db.relationship("UserModel", back_populates="category_groups")

    def __init__(self, name: str, assigned: float, activity: float, user_id: int):
        self.name = name
        self.assigned = Decimal(assigned)
        self.activity = Decimal(activity)
        self.user_id = user_id

    def update_assigned(self, assigned: float):
        self.assigned = Decimal(assigned)

    def __repr__(self):
        return f"<Category Group: {self.name}, Assigned: {self.assigned:.2f}, Activity: {self.activity:.2f}>"
