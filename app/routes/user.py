import datetime as dt
from flask import (
    jsonify, request, Blueprint, redirect, url_for, render_template,
    make_response, json, session
)
from app.services.user import user_signup_service, user_login_service
from app.utils.user_validator import generate_token
from app.utils.token_auth import user_token_required
from app.stores.service import get_service_store
from app.stores.appointment import find_user_byID
from app.utils.helpers import user_info_cookie
from app.utils.supabase_client import supabase

user_bp = Blueprint("user_bp", __name__, template_folder="../../templates")


# ---------- SIGNUP (POST) ----------
@user_bp.route('/register', methods=['POST'])
def user_signUp():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    result = user_signup_service(data)

    if isinstance(result, tuple):
        return result

    email = request.form.get("email")
    password = request.form.get("password")

    # Redirect to login page with email & password in query params
    return redirect(url_for("user_bp.show_user_login", email=email, password=password))


# ---------- LOGIN (POST) ----------
@user_bp.route("/login", methods=["POST"])
def user_login():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    result, status = user_login_service(data)

    # data_dict = json.loads(result[0].data.decode('utf-8'))

    if status != 200 and "error" in result:
        # Store error in session instead of passing directly
        session['login_error'] = result["error"]
        return redirect(url_for("admin_bp.show_admin_login",
                                email=data.get("email", ""),
                                password=data.get("password", "")))

    user_id = result.get('user', {}).get('id')

    token = generate_token({"user_id": user_id})

    user_info = result.get('user', {})
    # Convert list to JSON string
    user_info_str = json.dumps(user_info)

    resp = make_response(redirect(url_for("user_bp.show_user_dashboard")))
    resp.set_cookie(
        "UserToken",
        token,
        httponly=True,
        secure=False,
        samesite="Lax",  # less restrictive for testing
        path="/"
    )
    resp.set_cookie(
        "User_Info",
        user_info_str,
        httponly=True,
        secure=False,   # Change to True for HTTPS
        samesite="Strict"
    )
    return resp


@user_bp.route("/logout")
def user_logout():
    resp = make_response(redirect(url_for("user_bp.show_user_login")))
    resp.set_cookie(
        "UserToken",
        "",
        expires=0,
        httponly=True,
        secure=False,
        samesite="Strict",
        path="/"
    )
    resp.set_cookie(
        "User_Info",
        "",
        expires=0,
        httponly=True,
        secure=False,
        samesite="Strict",
        path="/"
    )
    return resp


# ---------- SIGNUP (GET) ----------
@user_bp.route("/signup", methods=["GET"])
def show_user_signup():
    return render_template("user/signup.html")


# ---------- LOGIN (GET) ----------
@user_bp.route("/login", methods=["GET"])
def show_user_login():
    email = request.args.get("email", "")
    password = request.args.get("password", "")

    error = session.pop('login_error', None)

    return render_template("user/login.html", email=email, password=password, error=error)


# ---------- DASHBOARD ----------
@user_bp.route("/services", methods=["GET"])
@user_token_required
def show_services():
    user_name = user_info_cookie("firstname")

    result = get_service_store()
    services = result.data

    return render_template("user/dashboard.html", user_name=user_name, services=services)


# ---------- DASHBOARD ----------
@user_bp.route("/", methods=["GET"])
@user_token_required
def show_user_dashboard():
    # ✅ Fetch Admin Info
    user_name = user_info_cookie("username")

    response = supabase.table("Admin").select("*").limit(1).execute()
    admin_data = response.data[0] if response.data else {}
    current_day = dt.datetime.now().strftime("%A")

    # ✅ Fetch Recent Appointments (limit 3 latest)
    appointments_response = (
        supabase.table("Appointment")
        .select("id, appointment_date, appointment_time, status, service_id, user_id, Service(name, price)")
        .order("appointment_date", desc=True)
        .limit(3)
        .execute()
    )

    recent_appointments = []
    if appointments_response.data:
        for appt in appointments_response.data:
            recent_appointments.append({
                "id": appt["id"],
                "appointment_date": appt["appointment_date"],
                "appointment_time": appt.get("appointment_time"),
                "status": appt.get("status", "pending"),
                "name": appt.get("Service", {}).get("name", "N/A"),
                "price": appt.get("Service", {}).get("price")
            })

    # ✅ Fetch Popular Services (just taking top 4 for now)
    services_response = supabase.table(
        "Service").select("*").limit(4).execute()
    popular_services = services_response.data if services_response.data else []

    # ✅ Fetch Schedule (Days + Slots)
    schedule_response = supabase.table("Schedule_days").select(
        "id, day_of_week, is_open, Schedule_time_slot(id, start_time, end_time)"
    ).execute()

    schedule_data = []
    if schedule_response.data:
        for day in schedule_response.data:
            schedule_data.append({
                "id": day["id"],
                "day_of_week": day["day_of_week"],
                "is_open": day["is_open"],
                "slots": [
                    {
                        "id": slot["id"],
                        "start_time": dt.datetime.strptime(slot["start_time"], "%H:%M:%S").strftime("%I:%M %p"),
                        "end_time": dt.datetime.strptime(slot["end_time"], "%H:%M:%S").strftime("%I:%M %p")
                    }
                    for slot in day.get("Schedule_time_slot", [])
                ]
            })

    return render_template(
        "user/aboutAdmin.html",
        admin=admin_data,
        user_name=user_name,
        recent_appointments=recent_appointments,
        popular_services=popular_services,
        schedule_data=schedule_data,
        current_day=current_day,
    )


# ---------- PROFILE ----------
@user_bp.route("/profile", methods=["GET"])
@user_token_required
def show_user_profile():
    user_name = user_info_cookie("firstname")
    user_id = user_info_cookie("id")

    user = find_user_byID(user_id).data

    return render_template("user/userProfile.html", user_name=user_name, user=user[0])
