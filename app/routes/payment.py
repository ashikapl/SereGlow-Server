from flask import jsonify, request, Blueprint
from app.services.payment import add_payment_service, get_payment_service, update_payment_service, delete_payment_service

payment_bp = Blueprint("payment_bp", __name__)


@payment_bp.route("/<int:appointment_id>", methods=["POST"])
def add_payment(service_id, appointment_id):
    data = request.get_json()

    result = add_payment_service(data, appointment_id)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201


@payment_bp.route("/<int:appointment_id>", methods=["GET"])
def get_payment(appointment_id):
    result = get_payment_service(appointment_id)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201


@payment_bp.route("/<int:appointment_id>/<int:payment_id>", methods=["PUT"])
def update_payment(appointment_id, payment_id):
    data = request.get_json()

    result = update_payment_service(data, appointment_id, payment_id)

    if isinstance(result, tuple):
        return result

    return jsonify({"message": "Update successful!"}), 200


@payment_bp.route("/<int:appointment_id>/<int:payment_id>", methods=["DELETE"])
def delete_payment(appointment_id, payment_id):
    result = delete_payment_service(appointment_id, payment_id)

    if isinstance(result, tuple):
        return result

    return jsonify({"message": "Delete successful!"}), 200
