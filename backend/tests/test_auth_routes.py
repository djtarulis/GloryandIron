import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_user():
    response = client.post("/auth/register", data={"username": "testuserB", "password": "testpassB"})
    assert response.status_code == 200
    assert "msg" in response.json() or "access_token" in response.json()

def test_login_user():
    # Ensure user exists
    client.post("/auth/register", data={"username": "testuserA", "password": "testpassA"})
    response = client.post("/auth/token", data={"username": "testuserA", "password": "testpassA"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_wrong_password():
    client.post("/auth/register", data={"username": "testuser3", "password": "testpass3"})
    response = client.post("/auth/token", data={"username": "testuser3", "password": "wrongpass"})
    assert response.status_code == 401 or response.status_code == 400

def test_profile_endpoint():
    # Register and login to get token
    client.post("/auth/register", data={"username": "testuserA", "password": "testpassA"})
    login = client.post("/auth/token", data={"username": "testuserA", "password": "testpassA"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/users/me", headers=headers)
    assert response.status_code == 200
    assert "username" in response.json()