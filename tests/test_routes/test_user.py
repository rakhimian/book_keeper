from app.schemas import user as user_schema


def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "test123@gmail.com", "password": "123"})
    new_user = user_schema.UserOut(**res.json())
    assert new_user.email == "test123@gmail.com"
    assert res.status_code == 201


def test_get_user(authorized_client):
    res = authorized_client.get(
        "/users/1")
    print(res.json())
    # user = user_schema.UserOut(**res.json())
    assert res.status_code == 200
