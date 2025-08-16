from flask import (
    jsonify, request, Blueprint, redirect, url_for, render_template,
    make_response, json, flash
)
from app.services.admin import admin_signup_service, admin_login_service
from app.utils.user_validator import generate_token
from app.utils.token_auth import admin_token_required

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

    data_dict = json.loads(result[0].data.decode('utf-8'))

    if isinstance(result, tuple) and "error" in data_dict:
        return jsonify({"message": "Login Failed!", "error": data_dict["error"]}), 401
        # return redirect(url_for("admin_bp.show_admin_login"))

    print("res", data_dict)
    admin_id = data_dict.get('admin', {}).get('id')

    token = generate_token({"user_id": admin_id})

    admin_info = data_dict.get('admin', {})
    # Convert list to JSON string
    admin_info_str = json.dumps(admin_info)

    resp = make_response(redirect(url_for("admin_bp.show_admin_dashboard")))
    resp.set_cookie(
        "AdminToken",
        token,
        httponly=True,
        secure=False,   # Change to True for HTTPS
        samesite="Strict"
    )
    resp.set_cookie(
        "Admin_Info",
        admin_info_str,
        httponly=True,
        secure=False,   # Change to True for HTTPS
        samesite="Strict"
    )
    return resp


# ---------- LOGOUT ----------
# @admin_bp.route("/logout", methods=["GET"])
# def admin_logout():
#     resp = make_response(render_template("main.html"))
#     resp.delete_cookie("authToken", samesite="Strict")
#     return resp


@admin_bp.route("/logout")
def admin_logout():
    resp = make_response(redirect(url_for("admin_bp.show_admin_login")))
    resp.set_cookie(
        "AdminToken",
        "",
        expires=0,
        httponly=True,
        secure=False,
        samesite="Strict",
        path="/"
    )
    resp.set_cookie(
        "Admin_Info",
        "",
        expires=0,
        httponly=True,
        secure=False,
        samesite="Strict",
        path="/"
    )
    return resp


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
@admin_token_required
def show_admin_dashboard():
    admin_info = request.cookies.get("Admin_Info")
    if admin_info:
        admin_name = json.loads(admin_info)["firstname"]
        # print("ad", admin_name)
    return render_template("admin/dashboard.html", admin_name=admin_name)


# ---------- PROFILE ----------
@admin_bp.route("/profile", methods=["GET"])
@admin_token_required
def show_admin_profile():
    return render_template("admin/adminProfile.html")
