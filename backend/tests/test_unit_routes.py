import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_token():
    client.post("/auth/register", data={"username": "unittestuser", "password": "unittestpass"})
    response = client.post("/auth/token", data={"username": "unittestuser", "password": "unittestpass"})
    return response.json()["access_token"]

@pytest.fixture
def city_id(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/city/create", data={"name": "UnitCity", "x": 5, "y": 5}, headers=headers)
    return response.json()["city_id"]

def test_train_unit(auth_token, city_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(f"/unit/{city_id}/train", data={"unit_type": "Infantry", "quantity": 10}, headers=headers)
    assert response.status_code == 200
    assert "msg" in response.json() or "training_id" in response.json()

def test_unit_training_queue(auth_token, city_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(f"/unit/{city_id}/training_queue", headers=headers)
    assert response.status_code == 200
    assert "queue" in response.json()

def test_city_garrison(auth_token, city_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(f"/unit/{city_id}/garrison", headers=headers)
    assert response.status_code == 200
    assert "garrison"