from flask import jsonify, request, Blueprint
from app.services.admin import create_signup_service, get_all_admins_Service, create_service, get_all_services

admin_bp = Blueprint("admin_bp", __name__)


@admin_bp.route('/register', methods=['POST'])
def admin_signUp():
    data = request.get_json()

    result = create_signup_service(data)

    print("routes result: ", result)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201


# 📥 READ all admins
@admin_bp.route('/', methods=['GET'])
def get_all_admin():
    result = get_all_admins_Service()

    if not result.data:
        return jsonify({"Massage": "Empty"}), 400

    return jsonify(result.data), 201


@admin_bp.route('/service', methods=['POST'])
def service():
    data = request.get_json()

    result = create_service(data)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201

@admin_bp.route('/service', methods=['Get'])
def get_services():
    result = get_all_services()

    if not result.data:
        return jsonify({"Massage": "Empty"}), 400

    return jsonify(result.data), 201