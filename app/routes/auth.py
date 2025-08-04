from app.services.auth import login_service
from flask import jsonify, request, Blueprint
# from app.services.admin import create_signup_service, get_all_admins_Service

login_bp = Blueprint("auth_bp", __name__)

@login_bp.rotues("/login", methods=["POST"])
def create_login(user_id):
    data = request.get_json()

    result = login_service(data)

    if "error" in result:
        return jsonify({"message":"Login Failed!"}), 404
    return jsonify({"message":"Login Successfull!"})