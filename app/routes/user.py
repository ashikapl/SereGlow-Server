from flask import jsonify, request, Blueprint
from app.services.user import user_signup_service, user_login_service

user_bp = Blueprint("user_bp", __name__)

@user_bp.route('/register', methods=['POST'])
def user_signUp():
    data = request.get_json()

    result = user_signup_service(data)

    print("routers result: ", result)

    if isinstance(result, tuple):
        return jsonify(result), 404
    return jsonify(result.data), 201

@user_bp.rotues("/login", methods=["POST"])
def user_login():
    data = request.get_json()

    result = user_login_service(data)

    if "error" in result:
        return jsonify({"message":"Login Failed!"}), 404
    return jsonify({"message":"Login Successfull!"})