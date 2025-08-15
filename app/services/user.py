from flask import jsonify
from app.stores.user import user_signup_store
from app.utils.user_validator import user_validator, user_generate_token


def user_signup_service(data):
    try:
        result = user_signup_store(data)

        if result:
            return result
    except Exception as e:
        error_message = str(e)

        # Detect UNIQUE constraint violation (email already exists)
        if 'duplicate key value violates unique constraint' in error_message and 'users_email_key' in error_message:
            return {"error": "Email already exists"}, 409  # HTTP 409 Conflict

        return {"error": error_message}, 500


def user_login_service(data):
    try:
        user = user_validator(data["email"], data["password"], "User")
        if not user:
            return jsonify({"error": "Invalid user or password!"}), 401

        print("user: ", user)

        user_id = user["id"]
        token = user_generate_token(user_id)

        return jsonify({"token": token, "message": "Login Successfull"}), 200
    except Exception as e:
        print("Login Error", str(e))
        return {"error": str(e)}
