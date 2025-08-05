from flask import jsonify, request, Blueprint
from app.services.admin import admin_signup_service, admin_login_service

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route('/register', methods=['POST'])
def admin_signUp():
    data = request.get_json()

    result = admin_signup_service(data)

    print("routers result: ", result)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201

@admin_bp.route("/login", methods=["POST"])
def admin_login():
    data = request.get_json()

    result = admin_login_service(data)

    if "error" in result:
        return jsonify({"message": "Login Failed!"}), 404
    return jsonify({"message": "Login Successfull!"})
