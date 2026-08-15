def test_submit_contact_returns_201(flask_client):
    response = flask_client.post(
        "/api/contact/",
        json={"name": "Nguyen Van A", "email": "a@example.com", "message": "Hello"},
    )
    assert response.status_code == 201
    assert "contactId" in response.get_json()


def test_submit_contact_missing_fields_returns_400(flask_client):
    response = flask_client.post("/api/contact/", json={"name": "Nguyen Van A"})
    assert response.status_code == 400
