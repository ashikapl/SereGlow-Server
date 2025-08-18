from flask import jsonify, request, Blueprint
from app.services.payment import add_payment_service, get_payment_service, update_payment_service, delete_payment_service

payment_bp = Blueprint("payment_bp", __name__)


@payment_bp.route("/<int:appointment_id>", methods=["POST"])
def add_payment(appointment_id):
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


@payment_bp.route("/<int:appointment_id>/<int:id>", methods=["PUT"])
def update_payment(appointment_id, id):
    data = request.get_json()

    result = update_payment_service(data, appointment_id, id)

    if isinstance(result, tuple):
        return result

    return jsonify({"message": "Update successful!"}), 200


@payment_bp.route("/<int:appointment_id>/<int:id>", methods=["DELETE"])
def delete_payment(appointment_id, id):
    result = delete_payment_service(appointment_id, id)

    if isinstance(result, tuple):
        return result

    return jsonify({"message": "Delete successful!"}), 200


@payment_bp.route("/paymentFind/<int:appointment_id>", methods=["GET"])
def find_payment(appointment_id):
    result = get_payment_service(appointment_id)

    return result.data
