from flask import (
    jsonify, request, Blueprint, redirect, url_for, render_template,
    make_response, json
)
from app.services.admin import admin_signup_service, admin_login_service
from app.utils.user_validator import generate_token

admin_bp = Blueprint("admin_bp", __name__, template_folder="../../templates")


# ---------- SIGNUP (POST) ----------
@admin_bp.route('/register', methods=['POST'])
def admin_signUp():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    result = admin_signup_service(data)
    print("routers result: ", result)

    if isinstance(result, tuple):
        return result

    email = request.form.get("email")
    password = request.form.get("password")

    # Redirect to login page with email & password in query params
    return redirect(url_for("admin_bp.show_admin_login", email=email, password=password))


# ---------- LOGIN (POST) ----------
@admin_bp.route("/login", methods=["POST"])
def admin_login():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    result = admin_login_service(data)
    print("res", result[0])

    if isinstance(result, dict) and "error" in result:
        return jsonify({"message": "Login Failed!", "error": result["error"]}), 401
    
    data_dict = json.loads(result[0].data.decode('utf-8'))
    admin_id = data_dict['admin']['id'] 

    token = generate_token({"user_id": admin_id})

    resp = make_response(redirect(url_for("admin_bp.show_admin_dashboard")))
    resp.set_cookie(
        "authToken", 
        token,
        httponly=True,
        secure=False,   # Change to True for HTTPS
        samesite="Strict"
    )
    return resp


# ---------- LOGOUT ----------
@admin_bp.route("/logout", methods=["GET"])
def admin_logout():
    """Logs out the admin by clearing session and redirecting to main page."""
    return render_template("main.html")


# ---------- SIGNUP (GET) ----------
@admin_bp.route("/signup", methods=["GET"])
def show_admin_signup():
    return render_template("admin/signup.html")


# ---------- LOGIN (GET) ----------
@admin_bp.route("/login", methods=["GET"])
def show_admin_login():
    email = request.args.get("email", "")
    password = request.args.get("password", "")
    return render_template("admin/login.html", email=email, password=password)


# ---------- DASHBOARD ----------
@admin_bp.route("/", methods=["GET"])
def show_admin_dashboard():
    return render_template("admin/dashboard.html")
