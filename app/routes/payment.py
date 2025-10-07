from flask import (jsonify, request, Blueprint,
                   render_template, redirect, url_for, session)
import stripe
import os
from app.services.payment import add_payment_service, get_payment_service, get_user_payment_service, update_payment_status_service, delete_payment_service
from app.stores.service import get_service_byId
from app.stores.payment import find_user_byID
from app.services.appointment import add_appointment_service
from app.utils.helpers import admin_info_cookie, user_info_cookie, stripeProductPriceID
from app.utils.token_auth import user_token_required, admin_token_required

payment_bp = Blueprint("payment_bp", __name__)

LOCAL_DOMAIN = os.getenv("DOMAIN_URL", "http://127.0.0.1:8000") + "/payment"


# ---------------- Add Payment (User) ----------------
@payment_bp.route("/<int:appointment_id>", methods=["POST"])
@user_token_required
def add_payment(appointment_id):
    data = request.get_json()

    result = add_payment_service(data, appointment_id)

    if isinstance(result, tuple):
        return result

    return jsonify(result.data), 201


# ---------------- Get Admin Payment ----------------
@payment_bp.route("/admin", methods=["GET"])
@admin_token_required
def get_admin_payment():
    result = get_payment_service()

    if isinstance(result, tuple):  # error handling
        return result

    payments = result.data
    admin_name = admin_info_cookie("firstname")

    # Add service names and user names to each payment
    for payment in payments:
        # Service name
        service_data = get_service_byId(payment["service_id"])
        payment["service_name"] = service_data.data[0]["name"] if service_data.data else "Unknown Service"

        # User name
        user_data = find_user_byID(payment["user_id"])
        if isinstance(user_data, tuple) or not user_data.data:
            payment["user_name"] = "Unknown User"
        else:
            u = user_data.data[0]
            payment["user_name"] = f"{u['firstname']} {u['lastname']}"

    return render_template("admin/payment.html", payments=payments, admin_name=admin_name)


# ---------------- Get User Payment ----------------
@payment_bp.route("/user", methods=["GET"])
@user_token_required
def get_user_payment():
    user_id = user_info_cookie("id")
    result = get_user_payment_service(user_id)

    if isinstance(result, tuple):  # Error handling
        return result

    payments = result.data

    # Add service names to each payment
    for payment in payments:
        service_data = get_service_byId(payment["service_id"])
        payment["service_name"] = service_data.data[0]["name"] if service_data.data else "Unknown Service"

    username = user_info_cookie("username")
    return render_template("user/payment.html", payments=payments, username=username)


# ---------------- Update Payment Status ----------------
@payment_bp.route("/update_status/<int:payment_id>", methods=["POST"])
@admin_token_required
def update_payment_status(payment_id):
    data = request.get_json()
    new_status = data.get("status")

    if not new_status:
        return jsonify({"error": "Status is required"}), 400

    result = update_payment_status_service(
        payment_id, {"payment_status": new_status})

    if isinstance(result, tuple):  # error case
        return result

    return jsonify({"message": "Status updated successfully"}), 200


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
        service_name = request.form.get("service_name")
        service_price = request.form.get("service_price")

        STRIPE_PRICE_ID = stripeProductPriceID(service_name)
        print("Id", STRIPE_PRICE_ID)
        checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    "price": STRIPE_PRICE_ID,
                    "quantity": 1
                }
            ],
            mode="payment",
            success_url=LOCAL_DOMAIN + "/success",
            cancel_url=LOCAL_DOMAIN + "/cancel"
        )

    except Exception as e:
        return str(e)

    return redirect(checkout_session.url, code=303)


# ---------------- SHOW Payment ----------------
@payment_bp.route('/', methods=['GET'])
@admin_token_required
def show_payment():
    admin_name = admin_info_cookie('firstname')

    return render_template("admin/payment.html", admin_name=admin_name)


# ---------------- SHOW Checkout (User) ----------------
@payment_bp.route("/checkout/<int:service_id>", methods=["GET"])
@user_token_required
def show_checkout(service_id):
    service = find_service_route(service_id)

    return render_template("user/checkout.html", service_name=service[0].get('name'), service_price=service[0].get('price'))


# ---------------- Show Payment Success ----------------
@payment_bp.route("/success", methods=["GET"])
@user_token_required
def show_payment_success():
    appointment_data = session.get("appointment_data")

    result = add_appointment_service(appointment_data)

    service = find_service_route(appointment_data.get('service_id'))

    payment_data = {"user_id": appointment_data.get('user_id'), "service_id": appointment_data.get(
        'service_id'), "appointment_id": result.data[0].get('id'), "amount": service[0].get('price'), "payment_method": 'online', "payment_status": 'paid'}

    payment_result = add_payment_service(
        payment_data, result.data[0].get('id'))

    # return render_template("user/payment_success.html")
    return redirect(url_for("payment_bp.show_booking_summary", service_name=service[0].get('name'), service_price=service[0].get('price'), appointment_date=appointment_data.get(
        'appointment_date'), appointment_time=appointment_data.get(
        'appointment_time')))


# ---------------- Show Payment Cancle----------------
@payment_bp.route("/cancel", methods=["GET"])
@user_token_required
def show_payment_cancel():
    return render_template("user/payment_cancel.html")


# ---------------- Show Booking Summary----------------
@payment_bp.route("/bookingSummary", methods=["GET"])
@user_token_required
def show_booking_summary():
    service_name = request.args.get("service_name")
    service_price = request.args.get("service_price")
    appointment_date = request.args.get("appointment_date")
    appointment_time = request.args.get("appointment_time")

    return render_template(
        "user/booking_summary.html",
        service_name=service_name,
        service_price=service_price,
        appointment_date=appointment_date,
        appointment_time=appointment_time
    )


# ---------------- Find Payment ----------------
@payment_bp.route("/paymentFind", methods=["GET"])
def find_payment():
    result = get_payment_service()
    return jsonify(result.data if not isinstance(result, tuple) else [])


# ---------------- Find User By user_id ----------------
@payment_bp.route("/userFind/<int:user_id>", methods=["GET"])
def find_user(user_id):
    result = find_user_byID(user_id)
    return jsonify(result.data if not isinstance(result, tuple) else [])


# ---------------- Find Service By service_id ----------------
@payment_bp.route("/serviceFind/<int:service_id>", methods=["GET"])
def find_service_route(service_id):
    result = get_service_byId(service_id)
    return result.data if not isinstance(result, tuple) else []
