from flask import jsonify, request, Blueprint, render_template
from app.services.feedback import add_feedback_service, get_feedback_service, update_feedback_service, delete_feedback_service

feedback_bp = Blueprint("feedback_bp", __name__)


@feedback_bp.route("/<int:service_id>", methods=["POST"])
def add_feedback(service_id):
    data = request.get_json()

    result = add_feedback_service(data, service_id)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201


@feedback_bp.route("/<int:service_id>", methods=["GET"])
def get_feedback(service_id):
    result = get_feedback_service(service_id)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data)


@feedback_bp.route("/<int:service_id>/<int:id>", methods=["PUT"])
def update_feedback(service_id, id):
    data = request.get_json()
    result = update_feedback_service(data, service_id, id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify({"message": "Updated Succcessfully!"}), 201


@feedback_bp.route("/<int:service_id>/<int:id>", methods=["DELETE"])
def delete_feedback(service_id, id):
    result = delete_feedback_service(service_id, id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify({"message": "Deleted Successfully!"}), 201


@feedback_bp.route("/", methods=["GET"])
def show_feedback():
    return render_template("admin/feedback.html")


@feedback_bp.route("/addFeedback", methods=["GET"])
def show_addFeedback():
    return render_template("user/addFeedback.html")
