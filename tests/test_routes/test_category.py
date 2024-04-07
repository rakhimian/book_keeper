from app.schemas import category as category_schema

json_data = {
    "name": "string",
    "parent": 0
}


def test_get_all_categories(authorized_client):
    res = authorized_client.get("/categories/")
    assert res.status_code == 200


def test_create_category(authorized_client):
    res = authorized_client.post(
        "/categories/", json=json_data)
    # new_category = category_schema.CategoryOut(**res.json())
    # print(new_category)
    assert res.status_code == 201
