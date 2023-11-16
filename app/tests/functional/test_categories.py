import json

from app.tests.conftest import load_response

headers = {"Content-Type": "application/json", "Accept": "application/json"}


def test_new_category_group(test_client, data):
    header = headers.copy()

    for user in data["users"]:
        header["Authorization"] = user["access_token"]

        response = test_client.get(f"/group", headers=header)
        assert response.status_code == 200

        response_data = load_response(response)
        assert len(response_data) == len(user["groups"])

        for group in user["groups"]:
            response = test_client.get(f"/group/{group['id']}", headers=header)
            assert response.status_code == 200

            response_data = load_response(response)
            assert response_data["name"] == group["name"]
            assert len(response_data["categories"]) == len(group["categories"])


def test_duplicate_group(test_client, data):
    user = data["users"][0]
    group = user["groups"][0]

    header = headers.copy()
    header["Authorization"] = user["access_token"]

    body = {"name": group["name"]}
    response = test_client.post(f"/group", data=json.dumps(body), headers=header)
    assert response.status_code == 409


def test_group_does_not_exist(test_client, data):
    user = data["users"][0]

    header = headers.copy()
    header["Authorization"] = user["access_token"]

    response = test_client.get(f"/group/1000", headers=header)
    assert response.status_code == 404


def test_add_category_to_group_that_does_not_exist(test_client, data):
    user = data["users"][0]

    header = headers.copy()
    header["Authorization"] = user["access_token"]

    body = {"name": "test", "category_group_id": "1000"}
    response = test_client.post("/category", data=json.dumps(body), headers=header)

    assert response.status_code == 404


def test_duplicate_category(test_client, data):
    user = data["users"][0]
    group = user["groups"][0]
    category = group["categories"][0]

    header = headers.copy()
    header["Authorization"] = user["access_token"]

    body = {"name": category["name"], "category_group_id": group["id"]}
    response = test_client.post("/category", data=json.dumps(body), headers=header)
    assert response.status_code == 409


def test_get_all_categories(test_client, data):
    user = data["users"][0]

    number_of_categories = 0
    for group in user["groups"]:
        number_of_categories += len(group["categories"])

    header = headers.copy()
    header["Authorization"] = user["access_token"]

    response = test_client.get(f"/category", headers=header)
    assert response.status_code == 200

    response_data = load_response(response)
    assert len(response_data) == number_of_categories
