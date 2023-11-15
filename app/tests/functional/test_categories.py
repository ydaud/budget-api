import json
from decimal import Decimal

from app.models import CategoryGroupModel

headers = {"Content-Type": "application/json", "Accept": "application/json"}


def test_new_category_group(test_client, user1):
    header = headers.copy()
    header["Authorization"] = user1["access_token"]
    data = {"name": "test", "assigned": 0.00, "activity": 0.00}
    response = test_client.post("/groups", data=json.dumps(data), headers=header)

    assert response.status_code == 201
    assert b"test" in response.data

    groups = CategoryGroupModel.query.all()
    assert len(groups) == 1
    assert groups[0].name == "test"
    assert groups[0].assigned == 0.00
    assert groups[0].activity == 0.00
