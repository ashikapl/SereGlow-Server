from flask import jsonify, request, Blueprint, render_template, json
from app.services.appointment import add_appointment_service, get_appointment_service, update_appointment_service, delete_appointment_service
from app.utils.supabase_client import supabase
from app.utils.token_auth import admin_token_required
from app.stores.service import get_service_store
from app.stores.appointment import find_user_byID, get_appointment_byUserID
from app.stores.service import get_service_byId
from app.utils.helpers import admin_info_cookie, user_info_cookie

appointment_bp = Blueprint("appointment_bp", __name__)


@appointment_bp.route("/<int:service_id>", methods=["POST"])
def add_appointment(service_id):
    data = request.get_json()

    result = add_appointment_service(data, service_id)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201


@appointment_bp.route("/", methods=["GET"])
def get_appointment():
    result = get_appointment_service()

    if isinstance(result, tuple):
        return result

    admin_name = admin_info_cookie('firstname')
    appointments = result.data

    # return jsonify(result.data), 200
    return render_template("admin/appointment.html", admin_name=admin_name, appointments=appointments)


@appointment_bp.route("/<int:service_id>/<int:id>", methods=["PUT"])
def update_appointment(service_id, id):
    data = request.get_json()

    result = update_appointment_service(data, service_id, id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify({"message": "Update successful!"}), 200


@appointment_bp.route("/<int:service_id>/<int:id>", methods=["DELETE"])
def delete_appointment(service_id, id):
    result = delete_appointment_service(service_id, id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify({"message": "Delete successful!"}), 200


@appointment_bp.route('/', methods=['GET'])
@admin_token_required
def show_appointment():
    admin_name = admin_info_cookie('firstname')

    return render_template("admin/appointment.html", admin_name=admin_name)


@appointment_bp.route("/booking", methods=["GET"])
def show_bookAppointment():
    service_id = request.args.get("service_id", type=int)
    user_name = user_info_cookie('username')

    result = get_service_store()
    services = result.data

    return render_template("user/bookAppointment.html", user_name=user_name, services=services, service_id=service_id)


@appointment_bp.route("/myappointment", methods=["GET"])
def show_myAppointment():
    user_name = user_info_cookie('username')
    user_id = user_info_cookie('id')

    result = get_appointment_byUserID(user_id)
    appointments = result.data

    return render_template("user/myAppointment.html", user_name=user_name, appointments=appointments)


@appointment_bp.route("/userFind/<int:user_id>", methods=["GET"])
def find_user(user_id):
    result = find_user_byID(user_id)

    return result.data


@appointment_bp.route("/serviceFind/<int:service_id>", methods=["GET"])
def find_service(service_id):
    result = get_service_byId(service_id)

    return result.data
