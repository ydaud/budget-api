from app.services import db


class CategoryGroupModel(db.Model):
    __tablename__ = "category_groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

    categories = db.relationship(
        "CategoryModel", back_populates="category_group", lazy="dynamic"
    )

    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), unique=False, nullable=False
    )
    user = db.relationship("UserModel", back_populates="category_groups")

    def __init__(self, name: str, user_id: int):
        self.name = name
        self.user_id = user_id

    def __repr__(self):
        return f"<Category Group: {self.name}>"
