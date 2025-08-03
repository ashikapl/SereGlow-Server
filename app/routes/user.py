from flask import jsonify, request, Blueprint
from app.services.user import create_signup_service, get_all_users_Service

user_bp = Blueprint("user_bp", __name__)


@user_bp.route('/register', methods=['POST'])
def user_signUp():
    data = request.get_json()

    result = create_signup_service(data)

    print("routes result: ", result)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201


# 📥 READ all admins
@user_bp.route('/', methods=['GET'])
def get_all_admin():
    result = get_all_users_Service()

    if not result.data:
        return jsonify({"Massage": "Empty"}), 400

    return jsonify(result.data), 201