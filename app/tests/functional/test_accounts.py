import json
from decimal import Decimal
from collections import Counter

from app.models import AccountModel

from app.tests.conftest import load_response

headers = {"Content-Type": "application/json", "Accept": "application/json"}


def test_accounts_added(test_client, data):
    header = headers.copy()

    for user in data["users"]:
        header["Authorization"] = user["access_token"]
        for account in user["accounts"]:
            response = test_client.get(f"/accounts/{account['id']}", headers=header)
            assert response.status_code == 200

            response_data = load_response(response)
            assert response_data["name"] == account["name"]
            assert response_data["balance"] == account["balance"]

            assert len(response_data["transactions"]) == len(account["transactions"])


def test_get_all_transactions(test_client, data):
    user = data["users"][0]
    accounts = user["accounts"]

    number_of_transactions = 0
    for account in accounts:
        number_of_transactions += len(account["transactions"])

    header = headers.copy()
    header["Authorization"] = user["access_token"]

    response = test_client.get("/transactions", headers=header)
    assert response.status_code == 200

    response_data = load_response(response)
    assert len(response_data) == number_of_transactions


def test_get_single_transaction(test_client, data):
    user = data["users"][0]
    account = user["accounts"][0]
    transaction = account["transactions"][0]

    header = headers.copy()
    header["Authorization"] = user["access_token"]

    response = test_client.get(f"/transactions/{transaction['id']}", headers=header)
    assert response.status_code == 200

    response_data = load_response(response)
    assert response_data["payee"] == transaction["payee"]
    assert response_data["date"] == transaction["date"]
    assert response_data["amount"] == transaction["amount"]
    assert response_data["inflow"] == transaction["inflow"]
    assert response_data["category"]["id"] == transaction["id"]


def test_get_single_transaction_does_not_exist(test_client, data):
    user = data["users"][0]

    header = headers.copy()
    header["Authorization"] = user["access_token"]

    response = test_client.get(f"/transactions/1000", headers=header)
    assert response.status_code == 404


def test_add_transaction_to_nonexistent_account(test_client, data):
    user = data["users"][0]

    header = headers.copy()
    header["Authorization"] = user["access_token"]

    body = {
        "account_id": "10000",
        "date": "2023-01-11",
        "payee": "test",
        "inflow": False,
        "amount": 1000.00,
        "category_id": 1,
    }
    response = test_client.post("/transactions", data=json.dumps(body), headers=header)
    assert response.status_code == 404


def test_add_transaction_to_nonexistent_category(test_client, data):
    user = data["users"][0]

    header = headers.copy()
    header["Authorization"] = user["access_token"]

    body = {
        "account_id": "10000",
        "date": "2023-01-11",
        "payee": "test",
        "inflow": False,
        "amount": 1000.00,
        "category_id": 100,
    }
    response = test_client.post("/transactions", data=json.dumps(body), headers=header)
    assert response.status_code == 404


def test_get_all_accounts(test_client, data):
    user = data["users"][0]

    header = headers.copy()
    header["Authorization"] = user["access_token"]

    response = test_client.get("/accounts", headers=header)
    assert response.status_code == 200

    response_data = load_response(response)
    assert len(response_data) == len(user["accounts"])


def test_duplicate_account(test_client, data):
    user = data["users"][0]
    account = user["accounts"][0]

    header = headers.copy()
    header["Authorization"] = user["access_token"]
    body = {"name": account["name"], "balance": 0.00, "type": account["type"]}
    response = test_client.post("/accounts", data=json.dumps(body), headers=header)

    assert response.status_code == 409


def test_get_nonexistent_account(test_client, data):
    user = data["users"][0]

    header = headers.copy()
    header["Authorization"] = user["access_token"]
    response = test_client.get("/accounts/1000", headers=header)

    assert response.status_code == 404


def test_update_account(test_client, data):
    user = data["users"][0]
    account = user["accounts"][0]

    header = headers.copy()
    header["Authorization"] = user["access_token"]

    update_data = {"id": account["id"], "name": "test update account"}
    response = test_client.put(
        f"/accounts/{account['id']}", data=json.dumps(update_data), headers=header
    )

    assert response.status_code == 200

    response = test_client.get(f"/accounts/{account['id']}", headers=header)
    assert response.status_code == 200

    response_data = load_response(response)
    assert response_data["name"] == "test update account"


def test_update_nonexistent_account(test_client, data):
    user = data["users"][0]

    header = headers.copy()
    header["Authorization"] = user["access_token"]

    update_data = {"id": 200, "name": "savings"}
    response = test_client.put(
        "/accounts/4", data=json.dumps(update_data), headers=header
    )

    assert response.status_code == 404


def test_update_account_with_same_name(test_client, data):
    user = data["users"][0]

    header = headers.copy()
    header["Authorization"] = user["access_token"]

    body = {"name": "same name", "balance": 0.00, "type": "saving"}
    response = test_client.post(f"/accounts", data=json.dumps(body), headers=header)

    assert response.status_code == 201

    response_data = load_response(response)

    update_data = {"id": response_data["id"], "name": "same name"}
    response = test_client.put(
        f"/accounts/{response_data['id']}", data=json.dumps(update_data), headers=header
    )

    assert response.status_code == 409
