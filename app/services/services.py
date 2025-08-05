from flask import jsonify
from app.stores.services import create_service_store, read_service_store


def create_service(data):
    try:
        result = create_service_store(data)

        if result:
            return result

    except Exception as e:
        error_message = str(e)

        # Detect UNIQUE constraint violation (email already exists)
        if 'duplicate key value violates unique constraint' in error_message and 'admin_email_key' in error_message:
            return {"error": "Email already exists"}, 409  # HTTP 409 Conflict

        return {"error": error_message}, 500


def read_services():
    try:
        result = read_service_store()

        if result:
            return result

    except Exception as e:
        return jsonify({"error": str(e)}), 500
