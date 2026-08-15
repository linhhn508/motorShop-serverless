import os

import jwt
from flask import Blueprint, jsonify, request

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "username and password required"}), 400

    if (
        data["username"] != os.environ.get("ADMIN_USERNAME")
        or data["password"] != os.environ.get("ADMIN_PASSWORD")
    ):
        return jsonify({"error": "invalid credentials"}), 401

    token = jwt.encode(
        {"sub": data["username"], "role": "admin"},
        os.environ.get("JWT_SECRET"),
        algorithm="HS256",
    )
    return jsonify({"token": token}), 200
