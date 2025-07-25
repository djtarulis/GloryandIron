import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_token():
    client.post("/auth/register", data={"username": "testuser", "password": "testpass"})
    response = client.post("/auth/token", data={"username": "testuser", "password": "testpass"})
    print("LOGIN RESPONSE:", response.status_code, response.text)  # Debug output
    assert response.status_code == 200, f"Login failed: {response.text}"
    assert "access_token" in response.json(), f"Response missing access_token: {response.text}"
    return response.json()["access_token"]

@pytest.fixture
def city_id(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/city/create", data={"name": "TestCity", "x": 10, "y": 20}, headers=headers)
    print("CITY CREATE RESPONSE:", response.status_code, response.text)  # Debug output
    assert response.status_code == 200, f"City creation failed: {response.text}"
    assert "city_id" in response.json(), f"Response missing city_id: {response.text}"
    return response.json()["city_id"]