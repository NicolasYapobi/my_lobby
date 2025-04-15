import pytest
from app import create_app
import os


@pytest.fixture
def client():
    app = create_app()
    app.secret_key = os.getenv("SECRET_KEY", "test_secret_key")
    with app.test_client(use_cookies=True) as client:
        with app.app_context():
            yield client


def test_login_success(client):
    response = client.post("/auth/login", json={"username": "testuser"})
    assert response.status_code == 200

    with client.session_transaction() as sess:
        assert sess["username"] == "testuser"

    client.post("/auth/logout")


def test_login_missing_username(client):
    response = client.post("/auth/login", json={})
    assert response.status_code == 400

    json_data = response.get_json()
    assert "Username required" in json_data["message"]


def test_login_already_exists(client):
    client.post("/auth/login", json={"username": "duplicate"})

    response = client.post("/auth/login", json={"username": "duplicate"})
    assert response.status_code == 400

    json_data = response.get_json()
    assert "Username already exists" in json_data["message"]

    client.post("/auth/logout")


def test_login_invalid_username(client):
    response = client.post("/auth/login", json={"username": "ab"})
    assert response.status_code == 400

    json_data = response.get_json()
    assert "Username must be between 3 and 20 characters" in json_data["message"]

    response = client.post("/auth/login", json={"username": "test@user"})
    assert response.status_code == 400

    json_data = response.get_json()
    assert "Username can only contain letters and numbers" in json_data["message"]


def test_logout_success(client):
    client.post("/auth/login", json={"username": "testuser"})

    logout_response = client.post("/auth/logout")
    assert logout_response.status_code == 200
    with client.session_transaction() as sess:
        assert "username" not in sess


def test_logout_not_logged_in(client):
    client.post("/auth/logout")

    response = client.post("/auth/logout")
    assert response.status_code == 401
    json_data = response.get_json()
    assert "User not connected" in json_data["message"]
