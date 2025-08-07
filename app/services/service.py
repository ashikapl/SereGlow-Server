from flask import jsonify
from app.stores.service import create_service_store, read_service_store, update_service_store, delete_service_store


def create_service_services(data):
    try:
        result = create_service_store(data)

        if result:
            return result

    except Exception as e:
        error_message = str(e)

        # Detect UNIQUE constraint violation (email already exists)
        if 'duplicate key value violates unique constraint' in error_message and 'Service_name_key' in error_message:
            return {"error": "Service Add Already"}, 409

        return {"error": error_message}, 500


def read_service_services():
    try:
        result = read_service_store()

        if result:
            return result

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def update_service_services(data, service_id):
    try:
        result = update_service_store(data, service_id)

        if result:
            return result

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def delete_service_services(service_id):
    try:
        result = delete_service_store(service_id)

        if result:
            return result

    except Exception as e:
        return jsonify({"error": str(e)}), 500
