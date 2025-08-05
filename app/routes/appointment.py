from flask import jsonify, request, Blueprint
from app.services.appointment import add_appointment_service, get_appointment_service, update_appointment_service, delete_appointment_service

appointment_bp = Blueprint("appointment_bp", __name__)

@appointment_bp.routes("/<int:service_id>", methods=["POST"])
def add_appointment(service_id):
    data = request.get_json()

    result = add_appointment_service(data, service_id)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201

@appointment_bp.routes("/<int:service_id>", methods=["GET"])
def get_appointment(service_id):
    result = get_appointment_service(service_id)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201

@appointment_bp.routes("/<int:service_id>/<int:id>", methods=["PUT"])
def update_appointment(service_id, id):
    data = request.get_json()

    result = update_appointment_service(data, service_id, id)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201

@appointment_bp.routes("/<int:service_id>/<int:id>", methods=["DELETE"])
def add_appointment(service_id, id):
    result = delete_appointment_service(service_id, id)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201

