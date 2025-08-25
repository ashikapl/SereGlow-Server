from flask import jsonify
from app.stores.schedule import add_schedule_store, get_schedule_store, update_schedule_store, delete_schedule_store


def add_schedule_service(data, id):
    try:
        result = add_schedule_store(data, id)
        if result:  # (error_dict, status_code)
            return result
        return {"data": result}, 201
    except Exception as e:
        error_message = str(e)
        if 'duplicate key value violates unique constraint' in error_message:
            return {"error": "Schedule Already Added!"}, 409
        return {"error": error_message}, 500


def get_schedule_service():
    try:
        result = get_schedule_store()
        # print("sche", result)

        if result:
            return result

    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500


def update_schedule_service(data, id):
    try:
        result = update_schedule_store(data, id)
        if isinstance(result, tuple):
            return result
        return {"data": result}, 200
    except Exception as e:
        return {"error": str(e)}, 500


def delete_schedule_service(id):
    try:
        result = delete_schedule_store(id)
        if isinstance(result, tuple):
            return result
        return {"data": result}, 200
    except Exception as e:
        return {"error": str(e)}, 500
