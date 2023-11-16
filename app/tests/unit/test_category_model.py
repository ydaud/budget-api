from app.models import CategoryGroupModel
from app.models import CategoryModel


def test_category_group(new_user):
    group = CategoryGroupModel(name="Living Expenses", user_id=new_user.id)

    assert group.name == "Living Expenses"
    assert group.user_id == new_user.id
    assert group.__repr__() == "<Category Group: Living Expenses>"


def test_category(new_user):
    group = CategoryGroupModel(name="Living Expenses", user_id=new_user.id)
    category = CategoryModel(name="Rent", category_group_id=group.id)

    assert category.name == "Rent"
    assert category.category_group_id == group.id
    assert category.__repr__() == "<Category: Rent>"
