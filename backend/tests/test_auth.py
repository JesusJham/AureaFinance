from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "activa" in response.json()["message"]


def test_register_and_login():
    payload = {
        "nombres": "Test",
        "apellidos": "User",
        "email": "test@aurea.com",
        "username": "testuser",
        "password": "secret123",
    }
    r = client.post("/api/auth/register", json=payload)
    assert r.status_code == 201

    r2 = client.post("/api/auth/login", json={"username": "testuser", "password": "secret123"})
    assert r2.status_code == 200
    assert "access_token" in r2.json()
