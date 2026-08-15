import os
import uuid

from flask import Blueprint, jsonify, request

from app.db import get_table

contact_bp = Blueprint("contact", __name__)


@contact_bp.route("/", methods=["POST"])
def submit_contact():
    data = request.get_json(silent=True) or {}
    if not all(k in data for k in ("name", "email", "message")):
        return jsonify({"error": "name, email, and message required"}), 400

    contact_id = str(uuid.uuid4())
    table = get_table(os.environ.get("CONTACTS_TABLE", "contacts"))
    table.put_item(Item={"contactId": contact_id, **data})
    return jsonify({"contactId": contact_id}), 201
