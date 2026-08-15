import json


def test_get_products_empty_returns_200(flask_client):
    response = flask_client.get("/api/products/")
    assert response.status_code == 200
    data = response.get_json()
    assert data["products"] == []


def test_get_products_returns_list(flask_client, dynamodb_tables):
    dynamodb_tables["products"].put_item(Item={
        "productId": "p1", "name": "Brake Pad", "category": "brakes", "price": 25
    })
    response = flask_client.get("/api/products/")
    assert response.status_code == 200
    assert len(response.get_json()["products"]) == 1


def test_get_product_by_id_returns_product(flask_client, dynamodb_tables):
    dynamodb_tables["products"].put_item(Item={
        "productId": "p1", "name": "Brake Pad", "category": "brakes", "price": 25
    })
    response = flask_client.get("/api/products/p1")
    assert response.status_code == 200
    assert response.get_json()["productId"] == "p1"


def test_get_product_by_id_not_found_returns_404(flask_client):
    response = flask_client.get("/api/products/nonexistent")
    assert response.status_code == 404


def test_search_products_by_name(flask_client, dynamodb_tables):
    dynamodb_tables["products"].put_item(Item={
        "productId": "p1", "name": "Brake Pad", "category": "brakes", "price": 25
    })
    response = flask_client.get("/api/products/?search=brake")
    assert response.status_code == 200
    assert len(response.get_json()["products"]) == 1


def test_create_product_requires_auth(flask_client):
    response = flask_client.post("/api/products/", json={"name": "New Part"})
    assert response.status_code == 401


def test_create_product_with_auth(flask_client, admin_token):
    response = flask_client.post(
        "/api/products/",
        json={"name": "Chain", "category": "drivetrain", "price": 15},
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    assert "productId" in response.get_json()


def test_delete_product_with_auth(flask_client, dynamodb_tables, admin_token):
    dynamodb_tables["products"].put_item(Item={"productId": "p1", "name": "Brake Pad"})
    response = flask_client.delete(
        "/api/products/p1",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
