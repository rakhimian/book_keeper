import pytest
from jose import jwt
from app.schemas import auth as auth_schema
from app.config import settings


def test_login_user(test_user, client):
    res = client.post(
        "/login/", data={"username": test_user['email'], "password": test_user['password']})
    token = auth_schema.Token(**res.json())
    payload = jwt.decode(token.access_token, settings.secret_key, algorithms=[settings.algorythm])
    user_id: str = payload.get("user_id")
    assert user_id == test_user['id']
    assert token.token_type == 'bearer'
    assert res.status_code == 200


# @pytest.mark.parametrize("email, password, status_code", [
#     ("wrongemail@gmail.com", "123", 401),
#     ("test123@gmail.com", "wrongPassword", 403),
#     # ("wrongemail@gmail.com", "wrongPassword", 401),
#     # (None, "123", 422),
#     # ("test123@gmail.com", None, 422),
# ])
# def test_incorrect_user(client, test_user, email, password, status_code):
#     res = client.post(
#         "/login/", data={"username": email, "password": password})
#
#     print(res.status_code)
#
#     assert res.status_code == status_code
#     # assert res.json().get("detail") == "Invalid credentials"

