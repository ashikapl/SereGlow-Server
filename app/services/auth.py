from flask import jsonify
from app.utils.user_validator import user_validator, generate_token


def login_service(data, table_name):
    try:
        user = user_validator(data["email"], data["password"], table_name)

        if not user:
            return jsonify({
                "success": False,
                "error": "Invalid user or password!"
            }), 401

        id = user["id"]

        token = generate_token(id)

        return jsonify({"token": token, "message": "Login Successfull"}), 201

    except Exception as e:
        print("Login Error", str(e))
        return {"error": str(e)}
