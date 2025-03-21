def test_get_user_by_id(client):
    response = client.get(
        "/user/1",
    )
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"
    # case user not found
    response = client.get(
        "/user/100",
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_by_id(client):
    response = client.get(
        "/user/1",
    )
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"
    # case user not found
    response = client.get(
        "/user/100",
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_update_user_by_id(client):
    response = client.put(
        "/user/1",
        json={
            "username": "updateuser",
            "email": "updateuser@example.com",
            "role": "user",
        },
    )
    assert response.status_code == 200
    assert response.json()["username"] == "updateuser"
    assert response.json()["email"] == "updateuser@example.com"

    # case user not found
    response = client.put(
        "/user/100",
        json={
            "username": "updateuser",
            "email": "updateuser@example.com",
            "role": "user",
        },
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

    # case user exists
    response = client.put(
        "/user/1",
        json={
            "username": "updateuser",
            "email": "updateuser!@example.com",
            "role": "user",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already exists"

    # case email exists
    response = client.put(
        "/user/1",
        json={
            "username": "updateuser!",
            "email": "updateuser@example.com",
            "role": "user",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already exists"


def test_delete_user_by_id(client):
    response = client.delete(
        "/user/1",
    )
    assert response.status_code == 200
    assert response.json()["username"] == "updateuser"
    # Try to get the deleted user
    response = client.get(
        "/user/1",
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
    # case user not found
    response = client.delete(
        "/user/100",
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
