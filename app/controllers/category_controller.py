import logging

from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint

from app import db
from app.models import CategoryGroupModel, CategoryModel
from app.schemas import CategoryGroupSchema, CategorySchema

LOG = logging.getLogger(__name__)

blp = Blueprint("Categories", "category", description="Operations on categories")


@blp.route("/group")
class Group(MethodView):
    @jwt_required()
    @blp.response(200, CategoryGroupSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        groups = CategoryGroupModel.query.filter_by(user_id=user_id).all()
        return groups

    @jwt_required()
    @blp.arguments(CategoryGroupSchema)
    @blp.response(201, CategoryGroupSchema)
    def post(self, group_data):
        name = group_data["name"]
        user_id = get_jwt_identity()

        CategoryGroupModel.query.filter_by(user_id=user_id, name=name).none_or_409(
            description="A group with that name already exists"
        )

        group = CategoryGroupModel(name, user_id)

        db.session.add(group)
        db.session.commit()

        return group


@blp.route("/group/<string:group_id>")
class Group(MethodView):
    @jwt_required()
    @blp.response(200, CategoryGroupSchema)
    def get(self, group_id):
        user_id = get_jwt_identity()
        group = CategoryGroupModel.query.filter_by(
            user_id=user_id, id=group_id
        ).first_or_404()
        return group


@blp.route("/category")
class Category(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        user_id = get_jwt_identity()

        categories = (
            CategoryModel.query.join(CategoryGroupModel)
            .filter(CategoryGroupModel.user_id == user_id)
            .all()
        )

        return categories

    @jwt_required()
    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, category_data):
        name = category_data["name"]
        category_group_id = category_data["category_group_id"]
        user_id = get_jwt_identity()

        CategoryGroupModel.query.filter_by(
            user_id=user_id, id=category_group_id
        ).first_or_404(description="A group with that id does not exist")

        CategoryModel.query.filter_by(
            category_group_id=category_group_id, name=name
        ).none_or_409(
            description="A category with that name already exists in this group"
        )

        category = CategoryModel(name, category_group_id)

        db.session.add(category)
        db.session.commit()

        return category
