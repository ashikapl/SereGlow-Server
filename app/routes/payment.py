from flask import jsonify, request, Blueprint, render_template, json
from app.services.payment import add_payment_service, get_payment_service, update_payment_service, delete_payment_service
from app.stores.service import get_service_byId
from app.stores.payment import find_user_byID
from app.utils.helpers import admin_info_cookie

payment_bp = Blueprint("payment_bp", __name__)


@payment_bp.route("/<int:appointment_id>", methods=["POST"])
def add_payment(appointment_id):
    data = request.get_json()

    result = add_payment_service(data, appointment_id)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201


@payment_bp.route("/", methods=["GET"])
def get_payment():
    result = get_payment_service()

    if isinstance(result, tuple):
        return result

    admin_name = admin_info_cookie('firstname')
    payments = result.data

    # return jsonify(result.data), 201
    return render_template("admin/payment.html", admin_name=admin_name, payments=payments)


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


@payment_bp.route('/', methods=['GET'])
def show_payment():
    admin_name = admin_info_cookie('fisrtname')

    return render_template("admin/payment.html", admin_name=admin_name)


@payment_bp.route("/paymentFind>", methods=["GET"])
def find_payment():
    result = get_payment_service()

    return result.data


@payment_bp.route("/userFind/<int:user_id>", methods=["GET"])
def find_user(user_id):
    result = find_user_byID(user_id)

    return result.data


@payment_bp.route("/serviceFind/<int:service_id>", methods=["GET"])
def find_service(service_id):
    result = get_service_byId(service_id)

    return result.data
