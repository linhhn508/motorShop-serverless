import os
from datetime import datetime, timezone

from boto3.dynamodb.conditions import Key
from flask import Blueprint, jsonify, request

from app.db import get_table

feedback_bp = Blueprint("feedback", __name__)


@feedback_bp.route("/", methods=["POST"])
def submit_feedback():
    data = request.get_json(silent=True) or {}
    if "productId" not in data:
        return jsonify({"error": "productId required"}), 400

    created_at = datetime.now(timezone.utc).isoformat()
    table = get_table(os.environ.get("FEEDBACK_TABLE", "feedback"))
    table.put_item(Item={"createdAt": created_at, **data})
    return jsonify({"message": "feedback submitted"}), 201


@feedback_bp.route("/<product_id>")
def get_feedback(product_id):
    table = get_table(os.environ.get("FEEDBACK_TABLE", "feedback"))
    response = table.query(
        KeyConditionExpression=Key("productId").eq(product_id)
    )
    return jsonify({"feedback": response.get("Items", [])}), 200
