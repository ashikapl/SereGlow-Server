from flask import jsonify, request, Blueprint, render_template
# import requests
from app.services.service import add_service_services, get_service_services, update_service_services, delete_service_services
from app.utils.token_auth import admin_token_required
from app.routes.admin import admin

service_bp = Blueprint("service_bp", __name__)


@service_bp.route('/', methods=['POST'])
@admin_token_required
def add_service():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    result = add_service_services(data)

    if isinstance(result, tuple):
        return result

    # return jsonify(result.data), 201
    return render_template("admin/service.html")


@service_bp.route('/', methods=['GET'])
@admin_token_required
def get_services():
    result = get_service_services()
    
    # print("name", admin["firstname"])
    # admin_na
    response = request.cookies.get("Admin_Info")
    print("res", response)
    # response = request.get('http://127.0.0.1:5000/admin/')
    # print("response", response.cookies.get_dict())

    if not result:
        return jsonify({"Massage": "Empty"}), 204

    # return jsonify(result.data), 200
    return render_template("admin/service.html", admin_name=response)


@service_bp.route('/<int:service_id>', methods=['PUT'])
@admin_token_required
def update_service(service_id):
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    result = update_service_services(data, service_id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify({"message": "Update successful!"}), 200


@service_bp.route('/<int:service_id>', methods=['DELETE'])
@admin_token_required
def delete_service(service_id):
    result = delete_service_services(service_id)

    # print("Rs", result)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify({"message": "Delete Successfull!"}), 200


@service_bp.route('/add', methods=['GET'])
@admin_token_required
def show_add_service():
    return render_template("admin/addService.html")


@service_bp.route('/update', methods=['GET'])
@admin_token_required
def show_update_service():
    return render_template("admin/updateService.html")
