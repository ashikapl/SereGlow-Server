from flask import jsonify
from app.stores.appointment import add_appointment_store, get_appointment_store, update_appointment_store, delete_appointment_store


def add_appointment_service(data, service_id):
    try:
        result = add_appointment_store(data, service_id)

        if result:
            return result

    except Exception as e:
        error_message = str(e)

        # Detect UNIQUE constraint violation (appointment already exists)
        if 'duplicate key value violates unique constraint' in error_message and 'appointment_name_key' in error_message:
            return {"error": "Appointment Already Added!"}, 409

        return {"error": error_message}, 500


def get_appointment_service(service_id):
    try:
        result = get_appointment_store(service_id)

        if result:
            return result

    except Exception as e:
        error_message = str(e)
        return {"error": error_message}, 500


def update_appointment_service(data, service_id, id):
    try:
        result = update_appointment_store(data, service_id, id)

        if result:
            return result

    except Exception as e:
        error_message = str(e)
        return {"error": error_message}, 500


def delete_appointment_service(service_id, id):
    try:
        result = delete_appointment_store(service_id, id)

        if result:
            return result

    except Exception as e:
        error_message = str(e)
        return {"error": error_message}, 500