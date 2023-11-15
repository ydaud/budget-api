import logging

from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort

from app import db
from app.models import CategoryGroupModel
from app.schemas import CategoryGroupSchema

LOG = logging.getLogger(__name__)

blp = Blueprint(
    "Category Groups", "category_groups", description="Operations on category groups"
)


@blp.route("/groups")
class AllGroups(MethodView):
    @jwt_required()
    @blp.response(200, CategoryGroupSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        groups = CategoryGroupSchema.query.filter_by(user_id=user_id).all()
        return groups

    @jwt_required()
    @blp.arguments(CategoryGroupSchema)
    @blp.response(201, CategoryGroupSchema)
    def post(self, group_data):
        name = group_data["name"]
        assigned = group_data["assigned"]
        activity = group_data["activity"]
        user_id = get_jwt_identity()

        query_name = CategoryGroupModel.query.filter_by(
            user_id=user_id, name=name
        ).first()
        if query_name:
            LOG.error(f"Group {name} already exists")
            abort(409, message="A group with that name already exists")

        group = CategoryGroupModel(name, assigned, activity, user_id)

        db.session.add(group)
        db.session.commit()

        return group
