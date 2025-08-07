from flask import jsonify, request, Blueprint
from app.services.payment import add_payment_service, get_payment_service, update_payment_service, delete_payment_service

payment_bp = Blueprint("payment_bp", __name__)


@payment_bp.route("/<int:service_id>", methods=["POST"])
def add_payment(service_id):
    data = request.get_json()

    result = add_payment_service(data, service_id)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201


@payment_bp.route("/<int:service_id>", methods=["GET"])
def get_payment(service_id):
    result = get_payment_service(service_id)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201


@payment_bp.route("/<int:service_id>/<int:id>", methods=["PUT"])
def update_payment(service_id, id):
    data = request.get_json()

    result = update_payment_service(data, service_id, id)

    if isinstance(result, tuple):
        return result

    return jsonify({"message": "Update successful!"}), 200


@payment_bp.route("/<int:service_id>/<int:id>", methods=["DELETE"])
def delete_payment(service_id, id):
    result = delete_payment_service(service_id, id)

    if isinstance(result, tuple):
        return result

    return jsonify({"message": "Delete successful!"}), 200
