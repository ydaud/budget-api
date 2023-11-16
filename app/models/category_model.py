from app.services import db


class CategoryModel(db.Model):
    __tablename__ = "category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    category_group_id = db.Column(
        db.Integer, db.ForeignKey("category_groups.id"), unique=False, nullable=False
    )
    category_group = db.relationship("CategoryGroupModel", back_populates="categories")

    transactions = db.relationship(
        "TransactionModel", back_populates="category", lazy="dynamic"
    )

    def __init__(self, name: str, category_group_id: int):
        self.name = name
        self.category_group_id = category_group_id

    def __repr__(self):
        return f"<Category: {self.name}>"
