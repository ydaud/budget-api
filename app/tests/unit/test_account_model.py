from app.models import AccountModel


def test_account(new_user):
    account = AccountModel(
        name="checking", balance=0.12, type="CHECKING", user_id=new_user.id
    )

    assert account.name == "checking"
    assert account.balance == 0.12
    assert account.type == "CHECKING"
    assert account.user_id == new_user.id
    assert account.__repr__() == f"<Account: checking, Balance: 0.12>"


def test_update_account(new_user):
    account = AccountModel(
        name="checking", balance=0.00, type="CHECKING", user_id=new_user.id
    )

    account.update(new_name="Joint")
    assert account.name == "Joint"
    assert account.type == "CHECKING"
    assert account.user_id == new_user.id

    account.update(new_type="SAVINGS")
    assert account.name == "Joint"
    assert account.type == "SAVINGS"

    account.update(new_name="test", new_type="CHECKING")
    assert account.name == "test"
    assert account.type == "CHECKING"


def test_add_balance(new_user):
    account = AccountModel(
        name="checking", balance=0.00, type="CHECKING", user_id=new_user.id
    )

    account.add_balance(100.00)
    assert account.balance == 100.00

    account.add_balance(-10.00)
    assert account.balance == 90
