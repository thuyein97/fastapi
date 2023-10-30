from fastapi.testclient import TestClient
from httpx import post
import pytest
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import schema
from app.databasetest import Base, get_db
from app.config import settings
from app import model
from app.oauth import create_access_token


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
model.Base.metadata.create_all(bind=engine)
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def session():
    model.Base.metadata.drop_all(bind=engine)
    model.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "test@gmail.com","password": "password"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(token, client):
    client.headers = {
        **client.headers,
        "authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_post(test_user, session):
    post_data = [
    {
        "title": "1st One",
        "content": "first content",
        "owner_id": test_user['id']
    },
    {
        "title": "2nd One",
        "content": "Second content",
        "owner_id": test_user['id']
    }]
    
    def create_post_data(post):
        return model.Post(**post)
    post_map = map(create_post_data, post_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(model.Post).all()
    return posts
    
    