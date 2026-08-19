SAMPLE_PRODUCT = {
    "id": "heo-dau-brembo-4-pis",
    "name": "Heo dầu Brembo 4 pis",
    "price": 118,
    "category": "Phanh & Thắng",
    "stock": 4,
    "product": {
        "overall": {
            "brand": "Brembo",
            "made_in": "Ý",
            "material": "Nhôm đúc CNC",
            "color": "Vàng",
        },
        "detail": "Heo dầu Brembo 4 piston hiệu suất phanh cao.",
    },
}

SAMPLE_PRODUCT_2 = {
    "id": "lop-michelin-city-grip-2",
    "name": "Lốp Michelin City Grip 2",
    "price": 244,
    "category": "Bánh & Lốp",
    "stock": 1,
    "product": {
        "overall": {
            "brand": "Michelin",
            "made_in": "Pháp",
            "material": "Cao su tổng hợp",
            "color": "Đen",
        },
        "detail": "Lốp Michelin City Grip 2 thế hệ mới.",
    },
}


def test_get_products_empty_returns_200(flask_client):
    response = flask_client.get("/api/products/")
    assert response.status_code == 200
    data = response.get_json()
    assert data == []


def test_get_products_returns_list(flask_client, dynamodb_tables):
    dynamodb_tables["products"].put_item(Item=SAMPLE_PRODUCT)
    response = flask_client.get("/api/products/")
    assert response.status_code == 200
    assert len(response.get_json()) == 1


def test_get_product_by_id_returns_product(flask_client, dynamodb_tables):
    dynamodb_tables["products"].put_item(Item=SAMPLE_PRODUCT)
    response = flask_client.get(f"/api/products/{SAMPLE_PRODUCT['id']}/info")
    assert response.status_code == 200
    data = response.get_json()
    assert data["id"] == SAMPLE_PRODUCT["id"]
    assert data["name"] == SAMPLE_PRODUCT["name"]
    assert data["category"] == SAMPLE_PRODUCT["category"]
    assert "product" in data


def test_get_product_by_id_not_found_returns_404(flask_client):
    response = flask_client.get("/api/products/nonexistent/info")
    assert response.status_code == 404


def test_search_products_by_name(flask_client, dynamodb_tables):
    dynamodb_tables["products"].put_item(Item=SAMPLE_PRODUCT)
    dynamodb_tables["products"].put_item(Item=SAMPLE_PRODUCT_2)
    response = flask_client.get("/api/products/?search=brembo")
    assert response.status_code == 200
    products = response.get_json()
    assert len(products) == 1
    assert products[0]["id"] == SAMPLE_PRODUCT["id"]


def test_search_products_by_category(flask_client, dynamodb_tables):
    from urllib.parse import urlencode
    dynamodb_tables["products"].put_item(Item=SAMPLE_PRODUCT)
    dynamodb_tables["products"].put_item(Item=SAMPLE_PRODUCT_2)
    qs = urlencode({"category": SAMPLE_PRODUCT["category"]})
    response = flask_client.get(f"/api/products/?{qs}")
    assert response.status_code == 200
    products = response.get_json()
    assert len(products) == 1
    assert products[0]["id"] == SAMPLE_PRODUCT["id"]


def test_create_product_requires_auth(flask_client):
    response = flask_client.post("/api/products/", json={"name": "New Part"})
    assert response.status_code == 401


def test_create_product_with_auth(flask_client, admin_token):
    payload = {
        "name": "Nhông sên dĩa DID vàng 428HD",
        "category": "Truyền động",
        "price": 442,
        "stock": 14,
        "product": {
            "overall": {
                "brand": "DID",
                "made_in": "Nhật Bản",
                "material": "Thép mạ vàng",
                "color": "Vàng",
            },
            "detail": "Bộ nhông sên dĩa DID 428HD mạ vàng.",
        },
    }
    response = flask_client.post(
        "/api/products/",
        json=payload,
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert "id" in data


def test_delete_product_with_auth(flask_client, dynamodb_tables, admin_token):
    dynamodb_tables["products"].put_item(Item=SAMPLE_PRODUCT)
    response = flask_client.delete(
        f"/api/products/{SAMPLE_PRODUCT['id']}",
        headers={"Authorization": f"Bearer {admin_token}"},
    )
    assert response.status_code == 200
