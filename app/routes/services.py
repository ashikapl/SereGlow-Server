from flask import jsonify, request, Blueprint
from app.services.services import create_serv_services, read_serv_services, update_serv_services, delete_serv_services
from app.utils.token_auth import token_required

service_bp = Blueprint("service_bp", __name__)


@service_bp.route('/', methods=['POST'])
# @token_required
def service():
    data = request.get_json()

    result = create_serv_services(data)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201


@service_bp.route('/', methods=['GET'])
@token_required
def get_services():
    result = read_serv_services()

    if not result.data:
        return jsonify({"Massage": "Empty"}), 204

    return jsonify(result.data), 200


@service_bp.route('/service/<int:service_id>', methods=['PUT'])
@token_required
def update_service(service_id):
    data = request.get_json()

    result = update_serv_services(data, service_id)

    if "error" in result:
        return jsonify({"message": "Update Failed!"}), 404

    return jsonify({"message": "Update Successfull!"})


@service_bp.route('/service/<int:service_id>', methods=['DELETE'])
@token_required
def delete_service(service_id):
    result = delete_serv_services(service_id)

    if "error" in result:
        return jsonify({"message": "Delete Failed!"}), 404

    return jsonify({"message": "Delete Successfull!"})
