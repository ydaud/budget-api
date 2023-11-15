from app.models import CategoryGroupModel


def test_category_group(new_user):
    group = CategoryGroupModel(
        name="Living Expenses", assigned=1000, activity=200, user_id=new_user.id
    )

    assert group.name == "Living Expenses"
    assert group.assigned == 1000
    assert group.activity == 200
    assert group.user_id == new_user.id
    assert (
        group.__repr__()
        == "<Category Group: Living Expenses, Assigned: 1000.00, Activity: 200.00>"
    )


def test_update_category_group(new_user):
    group = CategoryGroupModel(
        name="Living Expenses", assigned=1000, activity=200, user_id=new_user.id
    )

    group.update_assigned(assigned=200)
    assert group.assigned == 200
    assert group.activity == 200

    group.update_assigned(assigned=-200)
    assert group.assigned == -200
    assert group.activity == 200
