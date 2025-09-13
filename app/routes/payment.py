from flask import (jsonify, request, Blueprint,
                   render_template, json, redirect, url_for, session)
import stripe
from app.services.payment import add_payment_service, get_payment_service, update_payment_service, delete_payment_service
from app.stores.service import get_service_byId
from app.stores.payment import find_user_byID
from app.services.appointment import add_appointment_service
from app.utils.helpers import admin_info_cookie, user_info_cookie
from app.utils.token_auth import user_token_required

payment_bp = Blueprint("payment_bp", __name__)

LOCAL_DOMAIN = "http://127.0.0.1:8000/payment"


# ---------------- Add Payment (User) ----------------
@payment_bp.route("/<int:appointment_id>", methods=["POST"])
@user_token_required
def add_payment(appointment_id):
    data = request.get_json()

    result = add_payment_service(data, appointment_id)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201


# ---------------- Get Payment ----------------
@payment_bp.route("/", methods=["GET"])
def get_payment():
    result = get_payment_service()

    if isinstance(result, tuple):
        return result

    admin_name = admin_info_cookie('firstname')
    payments = result.data

    # return jsonify(result.data), 201
    return render_template("admin/payment.html", admin_name=admin_name, payments=payments)


# ---------------- Update Payment ----------------
@payment_bp.route("/<int:appointment_id>/<int:id>", methods=["PUT"])
def update_payment(appointment_id, id):
    data = request.get_json()

    result = update_payment_service(data, appointment_id, id)

    if isinstance(result, tuple):
        return result

    return jsonify({"message": "Update successful!"}), 200


# ---------------- Delete Payment ----------------
@payment_bp.route("/<int:appointment_id>/<int:id>", methods=["DELETE"])
def delete_payment(appointment_id, id):
    result = delete_payment_service(appointment_id, id)

    if isinstance(result, tuple):
        return result

    return jsonify({"message": "Delete successful!"}), 200


# ---------------- Payment Checkout Session ----------------
@payment_bp.route('/create-checkout-session', methods=['POST'])
@user_token_required
def create_checkout_session():
    try:

        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": 'price_1S6AfP8WAdI13hhpAk06INsV',
                    "quantity": 1
                }
            ],
            mode="subscription",
            success_url=LOCAL_DOMAIN + "/success",
            cancel_url=LOCAL_DOMAIN + "/cancle"
        )

    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


# ---------------- SHOW Payment ----------------
@payment_bp.route('/', methods=['GET'])
def show_payment():
    admin_name = admin_info_cookie('fisrtname')

    return render_template("admin/payment.html", admin_name=admin_name)


# ---------------- SHOW Checkout (User) ----------------
@payment_bp.route("/checkout/<int:service_id>", methods=["GET"])
@user_token_required
def show_checkout(service_id):
    service = find_service(service_id)

    return render_template("user/checkout.html", service_name=service[0].get('name'), service_price=service[0].get('price'))


# ---------------- Show Payment Success ----------------
@payment_bp.route("/success", methods=["GET"])
@user_token_required
def show_payment_success():
    appointment_data = session.get("appointment_data")
    print("appointment_data", appointment_data)

    result = add_appointment_service(appointment_data)

    service = find_service(appointment_data.get('service_id'))

    payment_data = {"user_id": appointment_data.get('user_id'), "service_id": appointment_data.get(
        'service_id'), "appointment_id": result.data[0].get('id'), "amount": service[0].get('price'), "payment_method": 'online', "payment_status": 'paid'}

    payment_result = add_payment_service(
        payment_data, result.data[0].get('id'))

    # return render_template("user/payment_success.html")
    return redirect(url_for("appointment_bp.show_myAppointment"))


# ---------------- Show Payment Cancle----------------
@payment_bp.route("/cancle", methods=["GET"])
@user_token_required
def show_payment_cancle():
    return render_template("user/payment_cancle.html")


# ---------------- Find Payment ----------------
@payment_bp.route("/paymentFind>", methods=["GET"])
def find_payment():
    result = get_payment_service()

    return result.data


# ---------------- Find User ----------------
@payment_bp.route("/userFind/<int:user_id>", methods=["GET"])
def find_user(user_id):
    result = find_user_byID(user_id)

    return result.data


# ---------------- Find Service ----------------
@payment_bp.route("/serviceFind/<int:service_id>", methods=["GET"])
def find_service(service_id):
    result = get_service_byId(service_id)

    return result.data
