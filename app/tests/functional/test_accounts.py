import json
from decimal import Decimal

from app.models import AccountModel

headers = {"Content-Type": "application/json", "Accept": "application/json"}


def test_new_account(test_client, user1):
    header = headers.copy()
    header["Authorization"] = user1["access_token"]
    data = {"name": "test", "balance": 0.00, "type": "checking"}
    response = test_client.post("/accounts", data=json.dumps(data), headers=header)

    assert response.status_code == 201
    assert b"test" in response.data

    accounts = AccountModel.query.all()
    assert len(accounts) == 1
    assert accounts[0].name == "test"


def test_duplicate_account(test_client, user1):
    header = headers.copy()
    header["Authorization"] = user1["access_token"]
    data = {"name": "test", "balance": 0.00, "type": "checking"}
    response = test_client.post("/accounts", data=json.dumps(data), headers=header)
    response = test_client.post("/accounts", data=json.dumps(data), headers=header)

    assert response.status_code == 409


def test_multiple_users(test_client, user1, user2):
    header = headers.copy()
    header["Authorization"] = user1["access_token"]
    data = {"name": "test", "balance": 0.00, "type": "checking"}
    response = test_client.post("/accounts", data=json.dumps(data), headers=header)

    assert response.status_code == 201
    assert b"test" in response.data
    assert b"test1@gmail.com" in response.data

    header["Authorization"] = user2["access_token"]
    data = {"name": "test", "balance": 0.00, "type": "checking"}
    response = test_client.post("/accounts", data=json.dumps(data), headers=header)

    assert response.status_code == 201
    assert b"test" in response.data
    assert b"test2@gmail.com" in response.data

    accounts = AccountModel.query.all()
    assert len(accounts) == 2


def test_update_account(test_client, user1):
    header = headers.copy()
    header["Authorization"] = user1["access_token"]
    data = {"name": "test", "balance": 0.00, "type": "checking"}
    test_client.post("/accounts", data=json.dumps(data), headers=header)

    update_data = {"id": 1, "name": "savings"}
    test_client.put("/accounts/1", data=json.dumps(update_data), headers=header)

    accounts = AccountModel.query.all()
    assert len(accounts) == 1
    assert accounts[0].name == "savings"


def test_update_nonexistent_account(test_client, user1):
    header = headers.copy()
    header["Authorization"] = user1["access_token"]

    update_data = {"id": 1, "name": "savings"}
    response = test_client.put(
        "/accounts/4", data=json.dumps(update_data), headers=header
    )

    assert response.status_code == 404


def test_add_transactions(test_client, user1):
    header = headers.copy()
    header["Authorization"] = user1["access_token"]
    data = {"name": "test", "balance": 0.00, "type": "checking"}
    test_client.post("/accounts", data=json.dumps(data), headers=header)

    transactions = [
        ["2023-02-11", "test1", True, 20.00, "1"],
        ["2023-02-12", "test2", False, 2.12, "1"],
        ["2023-02-13", "test3", True, 9.18, "1"],
        ["2023-02-14", "test4", False, 0.01, "1"],
        ["2023-02-15", "test5", True, 0.00, "1"],
    ]

    total = 0
    for t in transactions:
        data = {
            "date": t[0],
            "payee": t[1],
            "inflow": t[2],
            "amount": t[3],
            "account_id": t[4],
        }
        response = test_client.post(
            "/accounts/1/transactions", data=json.dumps(data), headers=header
        )

        assert response.status_code == 201

        amount = Decimal(t[3]) if t[2] else Decimal(t[3]) * -1
        total += round(amount, 2)

    response = test_client.get("/accounts", headers=header)
    assert f"{total}".encode() in response.data
