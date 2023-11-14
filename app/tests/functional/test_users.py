import json

from app.models import UserModel

headers = {"Content-Type": "application/json", "Accept": "application/json"}


def test_new_user(test_client):
    email = "ydaud@gmail.com"
    password = "password"
    data = {"email": email, "password": password}

    response = test_client.post("/register", data=json.dumps(data), headers=headers)
    assert response.status_code == 201

    users = UserModel.query.all()
    assert len(users) == 1
    assert users[0].email == email
    assert users[0].password != password
    assert users[0].__repr__() == f"<User: {email}>"


def test_duplicate_user(test_client_with_registered_user):
    data = {"email": "ydaud@gmail.com", "password": "password"}

    response = test_client_with_registered_user.post(
        "/register", data=json.dumps(data), headers=headers
    )
    assert response.status_code == 409


def test_wrong_format(test_client):
    data = {"email": "ydaudmail.com", "password": "password"}

    response = test_client.post("/register", data=json.dumps(data), headers=headers)
    assert response.status_code == 422


def test_multiple_users(test_client_with_registered_user):
    email = "yahya@gmail.com"
    password = "password"
    data = {"email": email, "password": password}

    response = test_client_with_registered_user.post(
        "/register", data=json.dumps(data), headers=headers
    )
    assert response.status_code == 201

    users = UserModel.query.all()
    assert len(users) == 2
    assert users[1].email == email
    assert users[1].password != password
    assert users[1].__repr__() == f"<User: {email}>"


def test_login(test_client_with_registered_user):
    data = {"email": "ydaud@gmail.com", "password": "password"}

    response = test_client_with_registered_user.post(
        "/login", data=json.dumps(data), headers=headers
    )
    assert response.status_code == 200
    assert b"access_token" in response.data


def test_login_error(test_client):
    data = {"email": "ydau@gmail.com", "password": "password"}

    response = test_client.post("/login", data=json.dumps(data), headers=headers)
    assert response.status_code == 401


def test_logout(test_client_with_registered_user):
    data = {"email": "ydaud@gmail.com", "password": "password"}

    response = test_client_with_registered_user.post(
        "/login", data=json.dumps(data), headers=headers
    )
    assert response.status_code == 200
    assert b"access_token" in response.data

    resp = response.data.decode().replace("'", '"')
    resp = json.loads(resp)
    access_token = resp["access_token"]

    header = {"Authorization": f"Bearer {access_token}"}

    response = test_client_with_registered_user.post("/logout", headers=header)
    assert response.status_code == 200

    header = {"Authorization": f"Bearer {access_token}"}

    response = test_client_with_registered_user.post("/logout", headers=header)
    assert response.status_code == 401


def test_logout_error(test_client):
    header = {"Authorization": f"Bearer wrongtoken"}

    response = test_client.post("/logout", headers=header)
    assert response.status_code == 401
