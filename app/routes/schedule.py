from flask import jsonify, request, Blueprint, render_template, json
from app.services.schedule import add_schedule_service, get_schedule_service, update_schedule_store, delete_schedule_service
from app.utils.helpers import admin_info_cookie

schedule_bp = Blueprint("schedule_bp", __name__)


@schedule_bp.route("/", methods=["POST"])
def add_schedule():
    data = request.get_json()

    result = add_schedule_service(data)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201


@schedule_bp.route("/", methods=["GET"])
def get_schedule():
    result = get_schedule_service()

    if isinstance(result, tuple):
        return result

    # return jsonify(result.data), 200
    admin_name = admin_info_cookie('firstname')

    Schedule_days = result[0].data
    Schedule_time_slot = result[1].data

    return render_template("admin/schedule.html", admin_name=admin_name, schedule_days=Schedule_days, schedule_time_slot=Schedule_time_slot)


@schedule_bp.route("/<int:id>", methods=["PUT"])
def update_schedule(service_id, id):
    data = request.get_json()

    result = update_schedule_store(data, id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify({"message": "Update successful!"}), 200


@schedule_bp.route("/<int:id>", methods=["DELETE"])
def delete_schedule(service_id, id):
    result = delete_schedule_service(id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify({"message": "Delete successful!"}), 200


@schedule_bp.route("/", methods=["GET"])
def show_schedule():
    admin_name = admin_info_cookie('firstname')

    return render_template("admin/schedule.html", admin_name=admin_name)
