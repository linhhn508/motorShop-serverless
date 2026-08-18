import os
import uuid
from functools import wraps

import jwt
from flask import Blueprint, jsonify, request

from app.db import get_table

products_bp = Blueprint("products", __name__)


def require_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "unauthorized"}), 401
        token = auth.split(" ", 1)[1]
        try:
            jwt.decode(token, os.environ.get("JWT_SECRET"), algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return jsonify({"error": "invalid token"}), 401
        return f(*args, **kwargs)
    return decorated


@products_bp.route("/")
def list_products():
    table = get_table(os.environ.get("PRODUCTS_TABLE", "products"))
    search = request.args.get("search", "").lower()
    category = request.args.get("category", "")

    if category:
        response = table.query(
            IndexName="category-index",
            KeyConditionExpression="category = :cat",
            ExpressionAttributeValues={":cat": category},
        )
        items = response.get("Items", [])
    else:
        response = table.scan()
        items = response.get("Items", [])

    if search:
        items = [i for i in items if search in i.get("name", "").lower()]

    return jsonify(items), 200


@products_bp.route("/categories/")
def list_categories():
    table = get_table(os.environ.get("PRODUCTS_TABLE", "products"))
    response = table.scan(ProjectionExpression="category")
    items = response.get("Items", [])
    print(items)
    categories = set(i.get("category") for i in items if i.get("category"))
    return jsonify(list(categories)), 200


@products_bp.route("/<product_id>/info")
def get_product(product_id):
    table = get_table(os.environ.get("PRODUCTS_TABLE", "products"))
    response = table.get_item(Key={"id": product_id})
    item = response.get("Item")
    if not item:
        return jsonify({"error": "product not found"}), 404
    return jsonify(item), 200


@products_bp.route("/", methods=["POST"])
@require_admin
def create_product():
    data = request.get_json(silent=True) or {}
    product_id = str(uuid.uuid4())
    item = {"id": product_id, **data}
    table = get_table(os.environ.get("PRODUCTS_TABLE", "products"))
    from decimal import Decimal
    if isinstance(item.get("price"), float):
        item["price"] = Decimal(str(item["price"]))
    table.put_item(Item=item)
    return jsonify({"id": product_id}), 201


@products_bp.route("/<product_id>", methods=["PUT"])
@require_admin
def update_product(product_id):
    data = request.get_json(silent=True) or {}
    table = get_table(os.environ.get("PRODUCTS_TABLE", "products"))
    response = table.get_item(Key={"id": product_id})
    if not response.get("Item"):
        return jsonify({"error": "product not found"}), 404
    table.put_item(Item={"id": product_id, **data})
    return jsonify({"id": product_id}), 200


@products_bp.route("/<product_id>", methods=["DELETE"])
@require_admin
def delete_product(product_id):
    table = get_table(os.environ.get("PRODUCTS_TABLE", "products"))
    table.delete_item(Key={"id": product_id})
    return jsonify({"message": "deleted"}), 200
