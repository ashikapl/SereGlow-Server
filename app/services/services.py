from flask import jsonify
from app.stores.services import add_service_store, get_service_store, update_service_store, delete_service_store

def add_service_services(data):
    try:
        result = add_service_store(data)

        if result:
            return result

    except Exception as e:
        error_message = str(e)

        # Detect UNIQUE constraint violation (email already exists)
        if 'duplicate key value violates unique constraint' in error_message and 'Service_name_key' in error_message:
            return {"error": "Service Add Already"}, 409

        return {"error": error_message}, 500

def get_service_services():
    try:
        result = get_service_store()

        if result:
            return result
        
        # print("result", result)

    except Exception as e:
        return {"error": str(e)}

def update_service_services(data, service_id):
    try:
        result = update_service_store(data, service_id)

        if result:
            return result

    except Exception as e:
        return {"error": str(e)}

def delete_service_services(service_id):
    try:
        result = delete_service_store(service_id)

        if result:
            return result

    except Exception as e:
        return jsonify({"error": str(e)}), 500
