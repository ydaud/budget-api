import logging
from datetime import datetime

from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint

from app import db
from app.models import (
    BudgetModel,
    MonthModel,
    EntryModel,
    CategoryGroupModel,
    CategoryModel,
)
from app.schemas import BudgetSchema, MonthSchema, EntrySchema, EntryUpdateSchema

LOG = logging.getLogger(__name__)

blp = Blueprint("Budget", "budgets", description="Operations on the budget")


@blp.route("/budget")
class Budget(MethodView):
    @jwt_required()
    @blp.response(200, BudgetSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        budgets = BudgetModel.query.filter_by(user_id=user_id).all()
        return budgets

    @jwt_required()
    @blp.arguments(BudgetSchema)
    @blp.response(201, BudgetSchema)
    def post(self, budget_data):
        name = budget_data["name"]
        user_id = get_jwt_identity()

        BudgetModel.query.filter_by(user_id=user_id, name=name).none_or_409(
            description="A budget with that name already exists"
        )

        budget = BudgetModel(name=name, user_id=user_id)

        db.session.add(budget)
        db.session.commit()

        return budget


@blp.route("/budget/<string:budget_id>/month")
class Month(MethodView):
    @jwt_required()
    @blp.response(200, MonthSchema(many=True))
    def get(self, budget_id):
        user_id = get_jwt_identity()
        months = (
            BudgetModel.query.filter_by(user_id=user_id, id=budget_id)
            .first_or_404(description="budget does not exist")
            .months.all()
        )

        return months

    @jwt_required()
    @blp.arguments(MonthSchema)
    @blp.response(201, MonthSchema)
    def post(self, month_data, budget_id):
        month = month_data["month"]
        user_id = get_jwt_identity()

        budget = BudgetModel.query.filter_by(id=budget_id).first_or_404(
            description="budget does not exist"
        )

        MonthModel.query.filter_by(budget_id=budget_id, month=month).none_or_409(
            description="month already exists"
        )

        month = MonthModel(month=month, budget_id=budget.id)

        db.session.add(month)

        categories = (
            CategoryModel.query.join(CategoryGroupModel)
            .add_columns(CategoryModel.id, CategoryGroupModel.user_id)
            .filter(CategoryGroupModel.user_id == user_id)
            .all()
        )

        for category in categories:
            entry = EntryModel(
                month_id=month.id,
                category_id=category.id,
                assigned=0.00,
                available=0.00,
            )
            db.session.add(entry)

        db.session.commit()

        return month


@blp.route("/budget/<string:budget_id>/month/<string:month>/entry")
class AllEntries(MethodView):
    @jwt_required()
    @blp.response(200, EntrySchema(many=True))
    def get(self, budget_id, month):
        user_id = get_jwt_identity()
        month = datetime.strptime(month, "%Y-%M").replace(minute=0)

        entries = (
            EntryModel.query.join(MonthModel)
            .join(BudgetModel)
            .filter(
                BudgetModel.user_id == user_id,
                BudgetModel.id == budget_id,
                MonthModel.month == month,
            )
            .all()
        )

        return entries


@blp.route("/budget/<string:budget_id>/month/<string:month>/entry/<string:entry_id>")
class Entry(MethodView):
    @jwt_required()
    @blp.response(200, EntrySchema)
    def put(self, budget_id, month, entry_id):
        user_id = get_jwt_identity()
        month = datetime.strptime(month, "%Y-%M").replace(minute=0)

        entry = (
            EntryModel.query.join(MonthModel)
            .joint(BudgetModel)
            .filter(
                BudgetModel.user_id == user_id,
                BudgetModel.id == budget_id,
                MonthModel.month == month,
                EntryModel.id == entry_id,
            )
            .firts_or_404(description="Entry does not exist")
        )

        return entry

    @jwt_required()
    @blp.arguments(EntryUpdateSchema)
    @blp.response(200, EntrySchema)
    def put(self, entry_update_data, budget_id, month, entry_id):
        user_id = get_jwt_identity()
        month = datetime.strptime(month, "%Y-%M").replace(minute=0)

        budget = BudgetModel.query.filter_by(
            user_id=user_id, id=budget_id
        ).first_or_404("Budget does not exist")

        entry = (
            EntryModel.query.join(MonthModel)
            .join(BudgetModel)
            .filter(
                BudgetModel.user_id == user_id,
                BudgetModel.id == budget_id,
                MonthModel.month == month,
                EntryModel.id == entry_id,
            )
            .first_or_404(description="Entry does not exist")
        )

        new_assigned = entry_update_data.get("assigned")

        budget.update_available(added_available=entry.assigned)
        budget.update_available(added_available=(new_assigned * -1))
        entry.update_assigned(new_assigned=new_assigned)

        db.session.add(entry)
        db.session.commit()

        return entry
