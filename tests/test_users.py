import pytest
from app import create_app
import os

@pytest.fixture
def client():
    app = create_app()
    app.secret_key = os.getenv("SECRET_KEY", "test_secret_key")

    with app.test_client() as client:
        client.environ_base["HTTP_COOKIE"] = ""
        with app.app_context():
            yield client


def test_get_users_unauthorized(client):
    response = client.get("/users/")
    assert response.status_code == 401


def test_get_users_success(client):
    client.post("/auth/login", json={"username": "testuser1"})

    response = client.get("/users/")
    assert response.status_code == 200

    json_data = response.get_json()
    assert json_data["count"] == 1

    users = json_data["users"]
    assert len(users) == 1
    assert "username" in users[0]
    assert "connected_at" in users[0]
