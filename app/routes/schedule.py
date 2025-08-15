from flask import jsonify, request, Blueprint, render_template
from app.services.appointment import add_appointment_service, get_appointment_service, update_appointment_service, delete_appointment_service

schedule_bp = Blueprint("schedule_bp", __name__)


@schedule_bp.route("/", methods=["GET"])
def show_schedule():
    return render_template("admin/schedule.html")
