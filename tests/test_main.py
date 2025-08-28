from fastapi.testclient import TestClient

# The client fixture is defined in conftest.py and is available automatically
def test_create_user(client: TestClient):
    response = client.post(
        "/users/", json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data
    assert "hashed_password" not in data  # Ensure password is not returned


def test_create_user_duplicate_email(client: TestClient):
    # First, create a user
    client.post(
        "/users/", json={"email": "test2@example.com", "password": "password123"}
    )
    # Then, try to create another user with the same email
    response = client.post(
        "/users/", json={"email": "test2@example.com", "password": "anotherpassword"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


def test_login_for_access_token(client: TestClient):
    # First, create a user to log in with
    client.post(
        "/users/", json={"email": "loginuser@example.com", "password": "testpassword"}
    )

    # Now, log in
    response = client.post(
        "/token",
        data={"username": "loginuser@example.com", "password": "testpassword"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_incorrect_password(client: TestClient):
    # Create a user
    client.post(
        "/users/",
        json={"email": "wrongpass@example.com", "password": "correctpassword"},
    )

    # Attempt to log in with the wrong password
    response = client.post(
        "/token",
        data={"username": "wrongpass@example.com", "password": "wrongpassword"},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect email or password"}


def test_read_users_me_unauthenticated(client: TestClient):
    response = client.get("/users/me")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_read_users_me_authenticated(client: TestClient):
    # Create user
    user_data = {"email": "authuser@example.com", "password": "authpassword"}
    client.post("/users/", json=user_data)

    # Log in to get token
    login_response = client.post(
        "/token",
        data={"username": user_data["email"], "password": user_data["password"]},
        headers={"content-type": "application/x-www-form-urlencoded"},
    )
    token = login_response.json()["access_token"]

    # Access protected route
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/users/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["is_active"] is True
    assert data["is_superuser"] is False
