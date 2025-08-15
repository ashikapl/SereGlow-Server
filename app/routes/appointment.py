from flask import jsonify, request, Blueprint, render_template
from app.services.appointment import add_appointment_service, get_appointment_service, update_appointment_service, delete_appointment_service
from app.utils.supabase_client import supabase

appointment_bp = Blueprint("appointment_bp", __name__)


@appointment_bp.route("/<int:service_id>", methods=["POST"])
def add_appointment(service_id):
    data = request.get_json()

    result = add_appointment_service(data, service_id)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201


@appointment_bp.route("/<int:service_id>", methods=["GET"])
def get_appointment(service_id):
    result = get_appointment_service(service_id)

    if isinstance(result, tuple):
        return result

    # return jsonify(result.data), 200
    return render_template("admin/manageAppointment.html")


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


@appointment_bp.route("/", methods=["GET"])
def show_appointment():
    result = supabase.table("Appointment").select("*").execute()

    if isinstance(result, tuple):
        return result

    # return jsonify(result.data), 200
    return render_template("admin/appointment.html")
