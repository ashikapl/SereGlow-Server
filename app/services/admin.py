from flask import jsonify
from app.stores.admin import admin_signup_store
from app.utils.user_validator import user_validator, admin_generate_token


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


# def admin_login_service(data):
#     try:
#         user = user_validator(data["email"], data["password"], "Admin")

#         if not user:
#             return jsonify({"error": "Invalid user or password!"}), 401

#         user_id = user["id"]
#         token = generate_token(user_id)

#         return jsonify({"token": token, "message": "Login Successfull"}), 200

#     except Exception as e:
#         print("Login Error", str(e))
#         return jsonify({"error": str(e)}), 500

def admin_login_service(data):
    try:
        user = user_validator(data["email"], data["password"], "Admin")

        if not user:
            return jsonify({"error": "Invalid user or password!"}), 401

        user_id = user["id"]
        print(user_id)
        token = admin_generate_token(user_id)

        return jsonify({"token": token, "message": "Login Successfull", "admin": user}), 200

    except Exception as e:
        print("Login Error", str(e))
        return jsonify({"error": str(e)}), 500
