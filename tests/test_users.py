from app import schema
from .database import client, session

def test_root(client):
    res = client.get("/")
    assert res.json().get("message") == "Hello World"
    assert res.status_code == 200
    
def test_user_create(client):
    res = client.post("/users/", json={"email": "hello@gmail.com", "password": "user"})
    new_user = schema.UserOut(**res.json())
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201
    
def test_login_user(client):
    res = client.post("/login", data={"username": "hello@gmail.com", "password": "user"})
    assert res.status_code == 200
    
    