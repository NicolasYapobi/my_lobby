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
    assert json_data["count"] >= 1

    users = json_data["users"]
    assert len(users) >= 1
    assert "username" in users[0]
    assert "connected_at" in users[0]


def test_get_users_sort_by_username(client):
    client.post("/auth/login", json={"username": "username1"})
    client.post("/auth/login", json={"username": "username2"})

    response = client.get("/users/?sort_by=username")
    assert response.status_code == 200

    json_data = response.get_json()
    users = json_data["users"]
    assert len(users) >= 2

    usernames = [user["username"] for user in users]
    sorted_usernames = sorted(usernames)
    assert usernames == sorted_usernames


def test_get_users_sort_by_connected_at(client):
    client.post("/auth/login", json={"username": "connectedAt1"})
    client.post("/auth/login", json={"username": "connectedAt2"})

    response = client.get("/users/?sort_by=connected_at")
    print(response.get_json())
    assert response.status_code == 200

    json_data = response.get_json()
    users = json_data["users"]
    assert len(users) >= 2

    connected_times = [user["connected_at"] for user in users]
    sorted_times = sorted(connected_times)
    assert connected_times == sorted_times


def test_get_users_invalid_sort_by(client):
    client.post("/auth/login", json={"username": "invalidSortBy1"})

    response = client.get("/users/?sort_by=invalid_field")
    assert response.status_code == 400
    assert "Invalid sort field" in response.get_json()["message"]
