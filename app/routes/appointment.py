from flask import (jsonify, request, Blueprint,
                   render_template, json,
                   redirect, url_for, session)
from app.services.appointment import (add_appointment_service, get_appointment_service,
                                      update_appointment_service, delete_appointment_service)
from app.utils.supabase_client import supabase
from app.utils.token_auth import admin_token_required, user_token_required
from app.stores.service import get_service_store
from app.stores.appointment import find_user_byID, get_appointment_byUserID
from app.stores.service import get_service_byId
from app.utils.helpers import admin_info_cookie, user_info_cookie
from app.services.payment import add_payment_service

appointment_bp = Blueprint("appointment_bp", __name__)


# ---------------- ADD APPOINTMENT ----------------
@appointment_bp.route("/", methods=["POST"])
def add_appointment():
    global appointment_data
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    service = find_service(data.get('service_id'))
    # print("service", service)

    # store in session
    print("appointment_data", data)
    session["appointment_data"] = data

    if data.get('payment_method') == "cash":
        print("cash")
        result = add_appointment_service(data)
        payment_data = {"user_id": data.get('user_id'), "service_id": data.get(
            'service_id'), "appointment_id": result.data[0].get('id'), "amount": service[0].get('price'), "payment_method": 'cash', "payment_status": 'pending'}
        payment_result = add_payment_service(
            payment_data, result.data[0].get('id'))
    elif data.get('payment_method') == "online":
        print("online")
        return redirect(url_for("payment_bp.show_checkout", service_id=service[0].get('id')))

    if isinstance(result, tuple):
        return result

    # return jsonify(result.data), 201
    return redirect(url_for("appointment_bp.show_myAppointment"))


# ---------------- GET APPOINTMENT ----------------
@appointment_bp.route("/", methods=["GET"])
def get_appointment():
    result = get_appointment_service()

    if isinstance(result, tuple):
        return result

    admin_name = admin_info_cookie('firstname')
    appointments = result.data

    # return jsonify(result.data), 200
    return render_template("admin/appointment.html",
                           admin_name=admin_name,
                           appointments=appointments)


# ---------------- UPDATE APPOINTMENT ----------------
@appointment_bp.route("/<int:service_id>/<int:id>", methods=["PUT"])
def update_appointment(service_id, id):
    data = request.get_json()

    result = update_appointment_service(data, service_id, id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    return jsonify({"message": "Update successful!"}), 200


# ---------------- DELETE APPOINTMENT ----------------
@appointment_bp.route("/delete/<int:service_id>/<int:id>", methods=["GET", "DELETE"])
def delete_appointment(service_id, id):
    result = delete_appointment_service(service_id, id)

    if isinstance(result, tuple):
        return jsonify(result[0]), result[1]

    # return jsonify({"message": "Delete successful!"}), 200
    return redirect(url_for("appointment_bp.show_myAppointment"))


# ---------------- SHOW APPOINTMENT (Admin) ----------------
@appointment_bp.route('/', methods=['GET'])
@admin_token_required
def show_appointment():
    admin_name = admin_info_cookie('firstname')

    return render_template("admin/appointment.html", admin_name=admin_name)


# ---------------- SHOW BOOK APPOINTMENT FROM (User) ----------------
@appointment_bp.route("/booking", methods=["GET"])
def show_bookAppointment():
    service_id = request.args.get("service_id", type=int)
    user_name = user_info_cookie('username')
    user_id = user_info_cookie('id')

    result = get_service_store()
    services = result.data

    return render_template("user/bookAppointment.html",
                           user_name=user_name,
                           user_id=user_id,
                           services=services,
                           service_id=service_id)


# ---------------- SHOW MY APPOINTMENT (User) ----------------
@appointment_bp.route("/myappointment", methods=["GET"])
@user_token_required
def show_myAppointment():
    user_name = user_info_cookie('username')
    user_id = user_info_cookie('id')
    print("user_id", user_id)

    result = get_appointment_byUserID(user_id)

    # Handle tuple (error case)
    if isinstance(result, tuple):
        # Instead of returning JSON, render page with empty list
        appointments = []
    else:
        appointments = result.data if result.data else []

    return render_template("user/myAppointment.html",
                           user_name=user_name,
                           appointments=appointments)


# ---------------- FIND USER BY ID ----------------
@appointment_bp.route("/userFind/<int:user_id>", methods=["GET"])
def find_user(user_id):
    result = find_user_byID(user_id)

    return result.data


# ---------------- FIND SERVICE BY ID ----------------
@appointment_bp.route("/serviceFind/<int:service_id>", methods=["GET"])
def find_service(service_id):
    result = get_service_byId(service_id)

    return result.data


# ---------------- UPDATE APPOINTMENT STATUS ----------------
@appointment_bp.route("/update_status/<int:id>", methods=["POST"])
def update_status(id):
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    new_status = data.get("status")

    print("data", data)

    try:
        response = supabase.table("Appointment").update(
            {"status": new_status}
        ).eq("id", id).execute()

        print("res", response)

        if response.data:
            return jsonify({"success": True, "message": "Status updated"})
        else:
            return jsonify({"success": False, "message": "No appointment found"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})
