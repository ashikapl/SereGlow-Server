from app.stores.payment import add_payment_store, get_payment_store, get_user_payment_store, update_payment_status_store, delete_payment_store


def add_payment_service(data, appointment_id):
    try:
        result = add_payment_store(data, appointment_id)

        if result:
            return result

    except Exception as e:
        error_message = str(e)

        # Detect UNIQUE constraint violation (appointment already exists)
        if 'duplicate key value violates unique constraint' in error_message and 'payment_name_key' in error_message:
            return {"error": "Payment Already Added!"}, 409

        return {"error": error_message}, 500


def get_payment_service():
    try:
        result = get_payment_store()

        if result:
            return result

    except Exception as e:
        error_message = str(e)
        return {"error": error_message}, 500


def get_user_payment_service(user_id):
    try:
        result = get_user_payment_store(user_id)

        if result:
            return result

    except Exception as e:
        error_message = str(e)
        return {"error": error_message}, 500


def update_payment_status_service(payment_id, data):
    try:
        result = update_payment_status_store(payment_id, data)
        return result
    except Exception as e:
        return {"error": str(e)}, 500


def delete_payment_service(appointment_id, id):
    try:
        result = delete_payment_store(appointment_id, id)

        if result:
            return result

    except Exception as e:
        error_message = str(e)

        return {"error": error_message}, 500
