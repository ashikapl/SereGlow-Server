from flask import jsonify, request, Blueprint, render_template, json
from app.services.appointment import add_appointment_service, get_appointment_service, update_appointment_service, delete_appointment_service
from app.utils.supabase_client import supabase
from app.utils.token_auth import admin_token_required
from app.stores.service import get_service_store
from app.stores.appointment import find_user_byID
from app.stores.service import get_service_byId
from app.stores.appointment import get_appointment_store
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

    admin_name = admin_info_cookie("firstname")

    if isinstance(result, tuple):
        return result

    appointments = result.data
    # print(appointments)
    # return jsonify(result.data), 200
    return render_template("admin/appointment.html", appointments=appointments, admin_name=admin_name)


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


# @appointment_bp.route("/", methods=["GET"])
# def show_appointment():
#     result = supabase.table("Appointment").select("*").execute()

#     if isinstance(result, tuple):
#         return result

#     # return jsonify(result.data), 200
#     return render_template("admin/appointment.html")

@appointment_bp.route('/', methods=['GET'])
# @admin_token_required
def show_appointment():
    return render_template("admin/appointment.html")


@appointment_bp.route("/booking", methods=["GET"])
def show_bookAppointment():
    service_id = request.args.get("service_id", type=int)
    # print("Service_id", service_id)
    user_name = user_info_cookie("firstname")

    result = get_service_store()
    services = result.data

    return render_template("user/bookAppointment.html", user_name=user_name, services=services, service_id=service_id)


@appointment_bp.route("/appointment", methods=["GET"])
def show_myAppointment():
    appointment_id = request.args.get("appointment_id", type=int)
    # print(appointment_id)
    user_name = user_info_cookie("firstname")

    result = get_appointment_store()
    appointments = result.data
    # print(appointments)

    return render_template("user/myAppointment.html", user_name=user_name, appointment_id=appointment_id, appointments=appointments)


@appointment_bp.route("/userFind/<int:user_id>", methods=["GET"])
def find_user(user_id):
    result = find_user_byID(user_id)

    return result.data


@appointment_bp.route("/serviceFind/<int:service_id>", methods=["GET"])
def find_service(service_id):
    result = get_service_byId(service_id)

    return result.data
