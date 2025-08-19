from flask import jsonify, request, Blueprint, render_template, json
from app.services.appointment import add_appointment_service, get_appointment_service, update_appointment_service, delete_appointment_service

schedule_bp = Blueprint("schedule_bp", __name__)


@schedule_bp.route("/", methods=["GET"])
def show_schedule():
    admin_info = request.cookies.get("Admin_Info")
    if admin_info:
        admin_name = json.loads(admin_info)["firstname"]
    return render_template("admin/schedule.html", admin_name=admin_name)
