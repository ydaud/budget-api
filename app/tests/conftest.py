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


@pytest.fixture(scope="function")
def test_client():
    os.environ["CONFIG_TYPE"] = "app.config.TestingConfig"
    app = create_app()
    app.logger.setLevel(100)

    with app.test_client() as testing_client:
        with app.app_context():
            db.create_all()
            yield testing_client
            db.drop_all()


@pytest.fixture(scope="function")
def test_client_with_registered_user(test_client):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {"email": "ydaud@gmail.com", "password": "password"}
    test_client.post("/register", data=json.dumps(data), headers=headers)

    yield test_client


def register_user(client, data, headers):
    client.post("/register", data=json.dumps(data), headers=headers)


def login(client, data, headers):
    response = client.post("/login", data=json.dumps(data), headers=headers)
    resp = response.data.decode().replace("'", '"')
    resp = json.loads(resp)
    access_token = resp["access_token"]

    return access_token


@pytest.fixture(scope="function")
def user1(test_client):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {"email": "test1@gmail.com", "password": "password"}

    register_user(test_client, data, headers)
    access_token = login(test_client, data, headers)

    data["access_token"] = "Bearer " + access_token

    yield data


@pytest.fixture(scope="function")
def user2(test_client):
    headers = {"Content-Type": "application/json", "Accept": "application/json"}
    data = {"email": "test2@gmail.com", "password": "password"}

    register_user(test_client, data, headers)
    access_token = login(test_client, data, headers)

    data["access_token"] = "Bearer " + access_token

    yield data


@pytest.fixture(scope="function")
def user1_with_data(test_client, user1):
    header = {"Content-Type": "application/json", "Accept": "application/json"}
    header["Authorization"] = user1["access_token"]
    data = {"name": "test1", "balance": 0.00, "type": "checking"}
    response = test_client.post("/accounts", data=json.dumps(data), headers=header)
    resp = response.data.decode().replace("'", '"')
    resp = json.loads(resp)

    transactions = [
        ["2023-02-11", "paycheque", True, 20.00, "1"],
        ["2023-02-12", "lights", False, 2.12, "1"],
        ["2023-02-13", "camera", True, 9.18, "1"],
        ["2023-02-14", "actors", False, 0.01, "1"],
        ["2023-02-15", "set", True, 0.00, "1"],
    ]

    for t in transactions:
        data = {
            "date": t[0],
            "payee": t[1],
            "inflow": t[2],
            "amount": t[3],
            "account_id": t[4],
        }
        test_client.post(
            f"/accounts/{resp['id']}/transactions",
            data=json.dumps(data),
            headers=header,
        )

    yield user1


@pytest.fixture(scope="function")
def user2_with_data(test_client, user2):
    header = {"Content-Type": "application/json", "Accept": "application/json"}
    header["Authorization"] = user2["access_token"]
    data = {"name": "test_account_1", "balance": 0.00, "type": "checking"}
    response = test_client.post("/accounts", data=json.dumps(data), headers=header)
    resp = response.data.decode().replace("'", '"')
    resp = json.loads(resp)

    transactions = [
        ["2023-02-11", "aaa", True, 10.00, "1"],
        ["2023-02-13", "gas", True, 6.01, "1"],
        ["2023-02-14", "rent", False, 1.01, "1"],
        ["2023-02-15", "test5", True, 2.00, "1"],
    ]

    for t in transactions:
        data = {
            "date": t[0],
            "payee": t[1],
            "inflow": t[2],
            "amount": t[3],
            "account_id": t[4],
        }
        test_client.post(
            f"/accounts/{resp['id']}/transactions",
            data=json.dumps(data),
            headers=header,
        )

    data = {"name": "test_account_2", "balance": 0.00, "type": "checking"}
    response = test_client.post("/accounts", data=json.dumps(data), headers=header)
    resp = response.data.decode().replace("'", '"')
    resp = json.loads(resp)

    transactions = [
        ["2023-02-11", "test1", True, 100.00, "1"],
        ["2023-02-13", "rent", True, 2000.00, "1"],
        ["2023-02-14", "help", False, 1000.00, "1"],
        ["2023-02-15", "me", True, 5400.00, "1"],
        ["2023-02-15", "zelle", False, 16.99, "1"],
    ]

    for t in transactions:
        data = {
            "date": t[0],
            "payee": t[1],
            "inflow": t[2],
            "amount": t[3],
            "account_id": t[4],
        }
        test_client.post(
            f"/accounts/{resp['id']}/transactions",
            data=json.dumps(data),
            headers=header,
        )

    yield user2
