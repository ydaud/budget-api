import json
import os

import pytest
from flask_jwt_extended import create_access_token

from app import create_app
from app.models import UserModel
from app.services import db

# --------
# Fixtures
# --------


@pytest.fixture(scope="module")
def new_user():
    user = UserModel(email="tester77@gmail.com", password="strong_password")
    return user


@pytest.fixture(scope="module")
def test_client():
    os.environ["CONFIG_TYPE"] = "app.config.TestingConfig"
    app = create_app()
    app.logger.setLevel(100)

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()


@pytest.fixture(scope="module")
def data(test_client):
    f = open("app/tests/resources/data.json")
    json_data = json.load(f)

    headers = {"Content-Type": "application/json", "Accept": "application/json"}

    for user in json_data["users"]:
        data = {"email": user["email"], "password": user["password"]}

        register_user(test_client, data, headers)
        access_token = login(test_client, data, headers)

        user["access_token"] = "Bearer " + access_token
        headers["Authorization"] = user["access_token"]

        for group in user["groups"]:
            data = {"name": group["name"]}
            response = test_client.post(
                "/group", data=json.dumps(data), headers=headers
            )
            response = load_response(response)
            group["id"] = response["id"]

            for category in group["categories"]:
                body = {"name": category["name"], "category_group_id": group["id"]}
                response = test_client.post(
                    "/category", data=json.dumps(body), headers=headers
                )
                response_data = load_response(response)
                category["id"] = response_data["id"]

        for account in user["accounts"]:
            body = {
                "name": account["name"],
                "balance": account["balance"],
                "type": account["type"],
            }
            response = test_client.post(
                "/accounts", data=json.dumps(body), headers=headers
            )
            response_data = load_response(response)
            account["id"] = response_data["id"]
            total = 0.00

            for transaction in account["transactions"]:
                body = {
                    "account_id": account["id"],
                    "date": transaction["date"],
                    "payee": transaction["payee"],
                    "inflow": transaction["inflow"],
                    "amount": transaction["amount"],
                    "category_id": transaction["category_id"],
                }
                response = test_client.post(
                    f"/transactions",
                    data=json.dumps(body),
                    headers=headers,
                )
                response_data = load_response(response)
                transaction["id"] = response_data["id"]

                if transaction["inflow"]:
                    total += transaction["amount"]
                else:
                    total -= transaction["amount"]

            account["balance"] = total

    return json_data


def load_response(response):
    resp = response.data.decode().replace("'", '"')
    resp = json.loads(resp)
    return resp


def register_user(client, data, headers):
    client.post("/register", data=json.dumps(data), headers=headers)


def login(client, data, headers):
    response = client.post("/login", data=json.dumps(data), headers=headers)
    response = load_response(response)
    access_token = response["access_token"]

    return access_token
