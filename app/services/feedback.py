from flask import jsonify
from app.stores.feedback import add_feedback_store, get_feedback_store, update_feedback_store, delete_feedback_store


def add_feedback_service(data, service_id):
    try:
        result = add_feedback_store(data, service_id)

        if result:
            return result

    except Exception as e:
        error_message = str(e)

        # Detect UNIQUE constraint violation (email already exists)
        if 'duplicate key value violates unique constraint' in error_message and 'feedback_name_key' in error_message:
            return {"error": "Service Add Already"}, 409

        return {"error": error_message}, 500


def get_feedback_service(service_id):
    try:
        result = get_feedback_store(service_id)

        if result:
            return result

    except Exception as e:
        return {"error": str(e)}, 500


def update_feedback_service(data, service_id, id):
    try:
        result = update_feedback_store(data, service_id, id)

        if result:
            return result

    except Exception as e:
        return {"error": str(e)}, 500


def delete_feedback_service(service_id, id):
    try:
        result = delete_feedback_store(service_id, id)

        if result:
            return result

    except Exception as e:
        return {"error": str(e)}, 500
