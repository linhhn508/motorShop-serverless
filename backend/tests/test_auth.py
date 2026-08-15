def test_login_valid_credentials_returns_token(flask_client):
    response = flask_client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "admin123"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data


def test_login_invalid_credentials_returns_401(flask_client):
    response = flask_client.post(
        "/api/auth/login",
        json={"username": "admin", "password": "wrongpassword"},
    )
    assert response.status_code == 401


def test_login_missing_body_returns_400(flask_client):
    response = flask_client.post("/api/auth/login", json={})
    assert response.status_code == 400
