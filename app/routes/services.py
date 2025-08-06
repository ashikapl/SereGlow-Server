from flask import jsonify, request, Blueprint
from app.services.services import add_service_services, get_service_services, update_service_services, delete_service_services
from app.utils.token_auth import token_required

service_bp = Blueprint("service_bp", __name__)

@service_bp.route('/', methods=['POST'])
# @token_required
def add_service():
    data = request.get_json()

    result = add_service_services(data)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201

@service_bp.route('/', methods=['GET'])
# @token_required
def get_service():
    result = get_service_services()

    # print("result", result)

    if "error" in result:
        return jsonify({"message": "No Service"}), 204

    return jsonify(result.data), 200

@service_bp.route('/<int:id>', methods=['PUT'])
# @token_required
def update_service(id):
    data = request.get_json()
    result = update_service_services(data, id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify({"message": "Update successful!"}), 200


@service_bp.route('/<int:id>', methods=['DELETE'])
# @token_required
def delete_service(id):
    result = delete_service_services(id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify({"message": "Delete Successfull!"})
