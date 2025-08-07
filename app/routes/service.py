from flask import jsonify, request, Blueprint
<<<<<<< HEAD:app/routes/services.py
from app.services.services import add_service_services, get_service_services, update_service_services, delete_service_services
=======
from app.services.service import create_service_services, read_service_services, update_service_services, delete_service_services
>>>>>>> 8d14f8a008a05a2fa1991986663335626cc0bfaa:app/routes/service.py
from app.utils.token_auth import token_required

service_bp = Blueprint("service_bp", __name__)


@service_bp.route('/service', methods=['POST'])
@token_required
def service():
    data = request.get_json()

<<<<<<< HEAD:app/routes/services.py
    result = add_service_services(data)
=======
    result = create_service_services(data)
>>>>>>> 8d14f8a008a05a2fa1991986663335626cc0bfaa:app/routes/service.py

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201

@service_bp.route('/', methods=['GET'])
# @token_required
<<<<<<< HEAD:app/routes/services.py
def get_service():
    result = get_service_services()
=======
def get_services():
    result = read_service_services()
>>>>>>> 8d14f8a008a05a2fa1991986663335626cc0bfaa:app/routes/service.py

@service_bp.route('/service', methods=['GET'])
@token_required
def get_services():
    result = add_service_services()

    if "error" in result:
        return jsonify({"message": "No Service"}), 204

    return jsonify(result.data), 200


<<<<<<< HEAD:app/routes/services.py
@service_bp.route('/service/<int:service_id>', methods=['PUT'])
@token_required
def update_service(service_id):
    data = request.get_json()

=======
@service_bp.route('/<int:service_id>', methods=['PUT'])
# @token_required
def update_service(service_id):
    data = request.get_json()
>>>>>>> 8d14f8a008a05a2fa1991986663335626cc0bfaa:app/routes/service.py
    result = update_service_services(data, service_id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify({"message": "Update successful!"}), 200


<<<<<<< HEAD:app/routes/services.py
@service_bp.route('/service/<int:service_id>', methods=['DELETE'])
@token_required
=======
@service_bp.route('/<int:service_id>', methods=['DELETE'])
# @token_required
>>>>>>> 8d14f8a008a05a2fa1991986663335626cc0bfaa:app/routes/service.py
def delete_service(service_id):
    result = delete_service_services(service_id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify({"message": "Delete Successfull!"})
