import random
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


@pytest.fixture
def authenticated_client(client):
    username = f"testuser{random.randint(0, 100)}"

    response = client.post("/auth/login", json={"username": username})
    assert response.status_code == 200

    with client.session_transaction() as sess:
        assert "username" in sess

    return client


def test_send_message_success(authenticated_client):
    response = authenticated_client.post("/messages/", json={"message": "Hello world!"})
    assert response.status_code == 200

    json_data = response.get_json()
    assert "Message sent successfully" in json_data["message"]


def test_send_message_unauthorized(client):
    response = client.post("/messages/", json={"message": "Hello world!"})
    assert response.status_code == 401

    json_data = response.get_json()
    assert "Unauthorized" in json_data["message"]


def test_send_empty_message(authenticated_client):
    response = authenticated_client.post("/messages/", json={"message": ""})
    assert response.status_code == 400

    json_data = response.get_json()
    assert "Empty message" in json_data["message"]


def test_send_message_missing_content(authenticated_client):
    response = authenticated_client.post("/messages/", json={})
    assert response.status_code == 400

    json_data = response.get_json()
    assert "Content required" in json_data["message"]
