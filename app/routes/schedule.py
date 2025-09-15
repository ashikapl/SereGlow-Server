from flask import jsonify, request, Blueprint, render_template, json, redirect, url_for
from app.services.schedule import add_schedule_service, get_schedule_service, update_schedule_service, delete_schedule_service
from app.utils.helpers import admin_info_cookie
from app.utils.token_auth import admin_token_required


schedule_bp = Blueprint("schedule_bp", __name__)


# ---------------- Add Schedule ----------------
@schedule_bp.route("/<int:id>", methods=["POST"])
@admin_token_required
def add_schedule(id):
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    result = add_schedule_service(data, id)

    if isinstance(result, tuple):
        return result
    if hasattr(result, "data"):
        return jsonify(result.data), 201
    # return jsonify(result), 201
    return redirect(url_for("schedule_bp.show_schedule"))


# ---------------- Get Schedule ----------------
@schedule_bp.route("/", methods=["GET"])
@admin_token_required
def get_schedule():
    result = get_schedule_service()

    if isinstance(result, tuple):
        return result  # already error

    # If result is string, load it into Python object
    if isinstance(result, str):
        result = json.loads(result)

    schedule_data = []
    for day in result:
        schedule_data.append({
            "id": day["id"],
            "day_of_week": day["day_of_week"],
            "is_open": day["is_open"],
            "slots": day.get("Schedule_time_slot", [])
        })

    return schedule_data


# ---------------- Update Schedule ----------------
@schedule_bp.route("/<int:id>", methods=["PUT"])
@admin_token_required
def update_schedule(id):
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    result = update_schedule_service(data, id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify({"message": "Update successful!"}), 200


# ---------------- Delete Schedule ----------------
@schedule_bp.route("/<int:id>", methods=["DELETE"])
@admin_token_required
def delete_schedule(id):
    result = delete_schedule_service(id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]
    return jsonify({"message": "Delete successful!"}), 200


# ---------------- Show Schedule ----------------
@schedule_bp.route("/show", methods=["GET"])
@admin_token_required
def show_schedule():
    admin_name = admin_info_cookie('firstname')
    schedule_data = get_schedule()

    return render_template(
        "admin/schedule.html",
        admin_name=admin_name,
        schedule_data=schedule_data
    )
