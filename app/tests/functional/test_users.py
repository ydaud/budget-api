import json

from app.models import UserModel

from app.tests.conftest import load_response


headers = {"Content-Type": "application/json", "Accept": "application/json"}


def test_new_user(test_client):
    body = {"email": "user_test@test.com", "password": "password"}

    response = test_client.post("/register", data=json.dumps(body), headers=headers)
    assert response.status_code == 201

    users = UserModel.query.all()
    assert users[0].email == body["email"]
    assert users[0].password != body["password"]
    assert users[0].__repr__() == f"<User: {body['email']}>"


def test_duplicate_user(test_client, data):
    user_email = data["users"][0]["email"]

    body = {"email": user_email, "password": "password"}
    response = test_client.post("/register", data=json.dumps(body), headers=headers)

    assert response.status_code == 409


def test_wrong_format(test_client):
    body = {"email": "ydaudmail.com", "password": "password"}

    response = test_client.post("/register", data=json.dumps(body), headers=headers)
    assert response.status_code == 422


def test_multiple_users(test_client, data):
    header = headers.copy()

    for user in data["users"]:
        header["Authorization"] = user["access_token"]
        response = test_client.get("/user", headers=header)

        assert response.status_code == 200

        response_data = load_response(response)
        assert response_data["email"] == user["email"]


def test_login(test_client, data):
    user_email = data["users"][0]["email"]

    body = {"email": user_email, "password": "password"}

    response = test_client.post("/login", data=json.dumps(body), headers=headers)
    assert response.status_code == 200
    assert b"access_token" in response.data


def test_login_error(test_client):
    data = {"email": "fail@test.com", "password": "password"}

    response = test_client.post("/login", data=json.dumps(data), headers=headers)
    assert response.status_code == 401


def test_logout(test_client, data):
    user = data["users"][0]

    header = headers.copy()
    header["Authorization"] = user["access_token"]

    response = test_client.post("/logout", headers=header)
    assert response.status_code == 200


def test_revoked_token(test_client, data):
    user = data["users"][0]

    header = headers.copy()
    header["Authorization"] = user["access_token"]

    response = test_client.post("/logout", headers=header)
    assert response.status_code == 401
