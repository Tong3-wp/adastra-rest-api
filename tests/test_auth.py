def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Server is running"}


def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword",
            "role": "user",
        },
    )
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"


def test_register_user_exist(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "new2@example.com",
            "password": "newpassword",
            "role": "user",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"


def test_register_email_exist(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser2",
            "email": "new@example.com",
            "password": "newpassword",
            "role": "user",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_login_for_access_token(client):
    response = client.post(
        "/auth/token",
        data={"username": "newuser", "password": "newpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_for_access_token_invalid_usename(client):
    response = client.post(
        "/auth/token",
        data={"username": "newuser!", "password": "newpassword"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_login_for_access_token_invalid_password(client):
    response = client.post(
        "/auth/token",
        data={"username": "newuser", "password": "newpassword!"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect username or password"


def test_get_current_user(client):
    login_response = client.post(
        "/auth/token",
        data={"username": "newuser", "password": "newpassword"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/user",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"
    assert response.json()["email"] == "new@example.com"
    assert response.json()["role"] == "user"


def test_get_current_user_unauthorized(client):
    response = client.get(
        "/auth/user",
        headers={"Authorization": "Bearer invalid_token"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"
