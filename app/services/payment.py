from flask import jsonify
from app.stores.payment import add_payment_store, get_payment_store, update_payment_store, delete_payment_store


def add_payment_service(data, service_id):
    try:
        result = add_payment_store(data, service_id)

        if result:
            return result

    except Exception as e:
        error_message = str(e)

        # Detect UNIQUE constraint violation (appointment already exists)
        if 'duplicate key value violates unique constraint' in error_message and 'payment_name_key' in error_message:
            return {"error": "Payment Already Added!"}, 409

        return {"error": error_message}, 500


def get_payment_service(service_id):
    try:
        result = get_payment_store(service_id)

        if result:
            return result

    except Exception as e:
        error_message = str(e)
        return {"error": error_message}, 500


def update_payment_service(data, service_id, id):
    try:
        result = update_payment_store(data, service_id, id)

        if result:
            return result

    except Exception as e:
        error_message = str(e)
        return {"error": error_message}, 500


def delete_payment_service(service_id, id):
    try:
        result = delete_payment_store(service_id, id)

        if result:
            return result

    except Exception as e:
        error_message = str(e)
        return {"error": error_message}, 500
