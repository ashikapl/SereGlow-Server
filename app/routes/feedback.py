from flask import render_template
from flask import (
    Blueprint, request, jsonify, render_template,
    redirect, url_for
)
from app.services.feedback import (
    add_feedback_service, get_feedback_service,
    update_feedback_service, delete_feedback_service
)
from app.stores.feedback import get_all_feedback_store
from app.utils.helpers import admin_info_cookie, user_info_cookie

feedback_bp = Blueprint("feedback_bp", __name__, url_prefix="/feedback")


# ---------------- ADD FEEDBACK ----------------
@feedback_bp.route("/<int:service_id>", methods=["POST"])
def add_feedback(service_id):
    """Handle feedback creation for a given service."""
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    result = add_feedback_service(data, service_id)
    if isinstance(result, tuple):  # Error returned
        return result

    return redirect(url_for("appointment_bp.show_myAppointment"))


# # ---------------- GET FEEDBACK ----------------
# @feedback_bp.route("/<int:service_id>", methods=["GET"])
# def get_feedback(service_id):
#     """Fetch feedback for a specific service."""
#     result = get_feedback_service(service_id)
#     print("res", result)
#     if isinstance(result, tuple):
#         return result
#     # return jsonify(result.data)
#     return redirect("admin/feedback.html", service_id=service_id), 200


# ---------------- GET FEEDBACK ----------------
@feedback_bp.route("/<int:service_id>", methods=["GET"])
def get_feedback(service_id):
    """Fetch feedback for a specific service."""
    user_id = user_info_cookie('id')
    # fetch feedback by service_id
    result = get_feedback_service(service_id, user_id)

    if isinstance(result, tuple):  # error case
        return result

    feedbacks = result.data if hasattr(result, "data") else result

    # Render HTML page and pass data to Jinja
    return render_template("admin/feedback.html",
                           user_id=user_id,
                           service_id=service_id,
                           feedbacks=feedbacks)


# ---------------- UPDATE FEEDBACK ----------------
@feedback_bp.route("/<int:service_id>/<int:id>", methods=["PUT"])
def update_feedback(service_id, id):
    """Update feedback by ID for a given service."""
    data = request.get_json() or {}
    result = update_feedback_service(data, service_id, id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify({"message": "Updated successfully!"}), 200


# ---------------- DELETE FEEDBACK ----------------
@feedback_bp.route("/<int:service_id>/<int:id>", methods=["DELETE"])
def delete_feedback(service_id, id):
    """Delete feedback by ID for a given service."""
    result = delete_feedback_service(service_id, id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify({"message": "Deleted successfully!"}), 200


# ---------------- SHOW ALL FEEDBACK (Admin) ----------------
@feedback_bp.route("/", methods=["GET"])
def show_feedback():
    """Admin view: list all feedback."""
    admin_name = admin_info_cookie("firstname")
    feedbacks = get_all_feedback_store().data

    return render_template("admin/feedback.html",
                           admin_name=admin_name,
                           feedbacks=feedbacks)


# ---------------- ADD FEEDBACK FORM (User) ----------------
@feedback_bp.route("/add/<int:service_id>", methods=["GET"])
def show_add_feedback(service_id):
    """User view: form to add feedback for a service."""
    user_name = user_info_cookie("username")
    user_id = user_info_cookie("id")

    return render_template("user/addFeedback.html",
                           user_name=user_name,
                           user_id=user_id,
                           service_id=service_id)
