from app.models import AccountModel, TransactionModel


def test_transaction():
    transaction = TransactionModel(
        date="20230228",
        payee="test",
        amount=10.12,
        inflow=True,
        account_id=1,
    )

    assert transaction.date == "20230228"
    assert transaction.payee == "test"
    assert transaction.amount == 10.12
    assert transaction.inflow == True
    assert transaction.account_id == 1
    assert transaction.raw_value == 10.12
    assert transaction.__repr__() == f"<Transaction: test 10.12>"


def test_amounts():
    transaction = TransactionModel(
        date="20230228",
        payee="test",
        amount=10.12,
        inflow=True,
        account_id=1,
    )

    assert transaction.amount == 10.12
    assert transaction.inflow == True
    assert transaction.raw_value == 10.12
    assert transaction.__repr__() == f"<Transaction: test 10.12>"

    transaction = TransactionModel(
        date="20230228",
        payee="test",
        amount=10.12,
        inflow=False,
        account_id=1,
    )

    assert transaction.amount == 10.12
    assert transaction.inflow == False
    assert transaction.raw_value == -10.12
    assert transaction.__repr__() == f"<Transaction: test -10.12>"

    transaction = TransactionModel(
        date="20230228",
        payee="test",
        amount=-10.12,
        inflow=True,
        account_id=1,
    )

    assert transaction.amount == 10.12
    assert transaction.inflow == False
    assert transaction.raw_value == -10.12
    assert transaction.__repr__() == f"<Transaction: test -10.12>"

    transaction = TransactionModel(
        date="20230228",
        payee="test",
        amount=-10.12,
        inflow=False,
        account_id=1,
    )

    assert transaction.amount == 10.12
    assert transaction.inflow == True
    assert transaction.raw_value == 10.12
    assert transaction.__repr__() == f"<Transaction: test 10.12>"
