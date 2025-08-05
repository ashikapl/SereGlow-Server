from flask import jsonify, request, Blueprint
from app.services.services import create_service, get_all_services

service_bp = Blueprint("service_bp", __name__)


@service_bp.route('/service', methods=['POST'])
def service():
    data = request.get_json()

    result = create_service(data)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201


@service_bp.route('/service', methods=['GET'])
def get_services():
    result = get_all_services()

    if not result.data:
        return jsonify({"Massage": "Empty"}), 400

    return jsonify(result.data), 201
