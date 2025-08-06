from flask import jsonify, request, Blueprint
from app.utils.token_auth import token_required
from app.services.appointment import add_appointment_service, get_appointment_service, update_appointment_service, delete_appointment_service

appointment_bp = Blueprint("appointment_bp", __name__)

@appointment_bp.route("/<int:service_id>", methods=["POST"])
# @token_required
def add_appointment(service_id):
    data = request.get_json()

    result = add_appointment_service(data, service_id)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201

@appointment_bp.route("/<int:service_id>", methods=["GET"])
# @token_required
def get_appointment(service_id):
    result = get_appointment_service(service_id)

    if "error" in result:
        return jsonify({"message": "No Appointment!"}), 204

    return jsonify(result.data), 200

@appointment_bp.route("/<int:service_id>/<int:id>", methods=["PUT"])
# @token_required
def update_appointment(service_id, id):
    data = request.get_json()

    result = update_appointment_service(data, service_id, id)

    if "error" in result:
        return jsonify({"message": "Updation Failed!"}), 404

    return jsonify({"message": "Update Successfull!"})

@appointment_bp.route("/<int:service_id>/<int:id>", methods=["DELETE"])
# @token_required
def delete_appointment(service_id, id):
    result = delete_appointment_service(service_id, id)

    if "error" in result:
        return jsonify({"message": "Deletion Failed!"}), 404

    return jsonify({"message": "Delete Successfull!"})

