from app.services.auth import login_service
from flask import jsonify, request, Blueprint

login_bp = Blueprint("login_bp", __name__)


@login_bp.route('/login/<int:table_number>', methods=['POST'])
def user_login(table_number):
    data = request.get_json()

    if table_number == 1:
        result = login_service(data, "Admin")
    elif table_number == 2:
        result = login_service(data, "User")

    # if "error" in result:
    #     return jsonify({"message":"Login Failed!"}), 404
    
    # return jsonify({"message":"Login Successfull!"})
    return result