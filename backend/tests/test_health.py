def test_health_returns_200(flask_client):
    response = flask_client.get("/api/health/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"