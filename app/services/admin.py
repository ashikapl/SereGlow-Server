from flask import jsonify
from app.stores.admin import admin_signup_store, update_admin_store
from app.utils.user_validator import user_validator, generate_token


def admin_signup_service(data):
    try:
        result = admin_signup_store(data)

        if result:
            return result

    except Exception as e:
        error_message = str(e)

        # Detect UNIQUE constraint violation (email already exists)
        if 'duplicate key value violates unique constraint' in error_message and 'admin_email_key' in error_message:
            return {"error": "Email already exists"}, 409  # HTTP 409 Conflict

        return {"error": error_message}, 500


def admin_login_service(data):
    try:
        user = user_validator(data["email"], data["password"], "Admin")

        if not user:
            return {"error": "Invalid user or password!"}, 401

        user_id = user["id"]
        token = generate_token(user_id)

        return {"token": token, "message": "Login Successfull", "admin": user}, 200

    except Exception as e:
        print("Login Error", str(e))
        # return jsonify({"error": str(e)}), 500
        return {"error": str(e)}, 500


def update_admin_service(data, id):
    try:
        result = update_admin_store(data, id)

        if result:
            return result

    except Exception as e:
        error_message = str(e)
        return {"error": error_message}, 500