import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_city(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/city/create", data={"name": "AnotherCity", "x": 20, "y": 25}, headers=headers)
    assert response.status_code == 200
    assert "city_id" in response.json()

def test_list_cities(auth_token):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get("/city/list", headers=headers)
    assert response.status_code == 200
    assert "cities" in response.json()

def test_get_city_details(auth_token, city_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.get(f"/city/{city_id}/city_details", headers=headers)
    assert response.status_code == 200
    assert "resources" in response.json()

def test_collect_resources(auth_token, city_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(f"/city/{city_id}/collect", headers=headers)
    assert response.status_code == 200
    assert "collected" in response.json()

def test_delete_city(auth_token, city_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.delete(f"/city/{city_id}/delete", headers=headers)
    assert response.status_code == 200
    assert "msg" in response.json()

def test_construct_building(auth_token, city_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post(f"/city/{city_id}/build", data={"building_type": "Warehouse"}, headers=headers)
    assert response.status_code == 200
    assert "building" in response.json()

def test_switch_active_city(auth_token, city_id):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = client.post("/city/switch_active_city", data={"city_id": city_id}, headers=headers)
    assert response.status_code == 200
    assert "active_city_id" in response.json()