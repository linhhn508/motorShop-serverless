def test_submit_feedback_returns_201(flask_client):
    response = flask_client.post(
        "/api/feedback/",
        json={"productId": "p1", "rating": 5, "comment": "Great part!"},
    )
    assert response.status_code == 201


def test_get_feedback_for_product(flask_client, dynamodb_tables):
    dynamodb_tables["feedback"].put_item(Item={
        "productId": "p1", "createdAt": "2026-08-15T10:00:00", "rating": 5, "comment": "Good"
    })
    response = flask_client.get("/api/feedback/p1")
    assert response.status_code == 200
    items = response.get_json()["feedback"]
    assert len(items) == 1


def test_submit_feedback_missing_productid_returns_400(flask_client):
    response = flask_client.post("/api/feedback/", json={"rating": 5})
    assert response.status_code == 400
