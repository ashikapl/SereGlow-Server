from flask import jsonify, request, Blueprint, render_template, json, redirect, url_for
from app.services.service import add_service_services, get_service_services, update_service_services, delete_service_services
from app.utils.token_auth import admin_token_required
from app.stores.service import get_service_byId
from app.utils.helpers import admin_info_cookie, stripeProductCreate


service_bp = Blueprint("service_bp", __name__)


# ---------------- Add Service ----------------
@service_bp.route('/', methods=['POST'])
@admin_token_required
def add_service():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    result = add_service_services(data)

    product = stripeProductCreate(
        name=result.data[0]['name'], description=result.data[0]['description'], price=result.data[0]['price'])

    if isinstance(result, tuple):
        return result

    # return jsonify(result.data), 201
    return redirect(url_for("service_bp.get_services"))


# ---------------- Get Service ----------------
@service_bp.route('/', methods=['GET'])
@admin_token_required
def get_services():
    result = get_service_services()

    admin_name = admin_info_cookie('firstname')

    if not result:
        return jsonify({"Massage": "Empty"}), 204

    services = result.data
    # return jsonify(result.data), 200
    return render_template("admin/service.html", admin_name=admin_name, services=services)


# ---------------- Update Service ----------------
@service_bp.route('/<int:service_id>', methods=['POST', "PUT"])
@admin_token_required
def update_service(service_id):
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    result = update_service_services(data, service_id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    # return jsonify({"message": "Update successful!"}), 200
    return redirect(url_for("service_bp.get_services"))


# ---------------- Delete Service ----------------
@service_bp.route('/delete/<int:service_id>', methods=['GET', 'DELETE'])
@admin_token_required
def delete_service(service_id):
    result = delete_service_services(service_id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    # return jsonify({"message": "Delete Successfull!"}), 200
    return redirect(url_for("service_bp.get_services"))


# ---------------- Show Add Service ----------------
@service_bp.route('/add', methods=['GET'])
@admin_token_required
def show_add_service():
    return render_template("admin/addService.html")


# ---------------- Show Update Service ----------------
@service_bp.route('/update', methods=['GET'])
@admin_token_required
def show_update_service():
    service_id = request.args.get("service_id", type=int)
    service = get_service_byId(service_id)

    return render_template("admin/updateService.html", service=service.data[0])
