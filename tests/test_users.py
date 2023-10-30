import email
import json
import pytest
from app import schema
# from .database import client, session
from app.config import settings
from jose import jwt



# def test_root(client):
#     res = client.get("/")
#     assert res.json().get("message") == "Hello World"
#     assert res.status_code == 200
    
def test_user_create(client):
    res = client.post("/users/", json={"email": "hello@gmail.com", "password": "password123"})
    new_user = schema.UserOut(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201
    
def test_login_user(client,test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_res = schema.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])

    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("email, passwords, status_code", [
    ('worng@gmail.com', 'password', 403),
    ('hello@gmail.com', 'password', 403),
    ('worng@gmail.com', 'wrong@gmail.com', 403),
    (None, 'password123', 422),
    ('hello@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, passwords, status_code):
    res = client.post("/login", data={"username": email, "password": passwords})
    
    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid Credentials"