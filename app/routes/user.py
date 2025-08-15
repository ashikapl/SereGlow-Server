from flask import (
    jsonify, request, Blueprint, redirect, url_for, render_template,
    make_response, json
)
from app.services.user import user_signup_service, user_login_service
from app.utils.user_validator import generate_token
from app.utils.token_auth import user_token_required

user_bp = Blueprint("user_bp", __name__, template_folder="../../templates")


# ---------- SIGNUP (POST) ----------
@user_bp.route('/register', methods=['POST'])
def user_signUp():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    result = user_signup_service(data)
    print("routers result: ", result)

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

    result = user_login_service(data)
    print("res", result[0])

    data_dict = json.loads(result[0].data.decode('utf-8'))

    if isinstance(result, tuple) and "error" in data_dict:
        return jsonify({"message": "Login Failed!", "error": data_dict["error"]}), 401
        # return redirect(url_for("user_bp.show_user_login"))

    # user_id = data_dict['user']['id']
    user_id = data_dict.get('user', {}).get('id')

    token = generate_token({"user_id": user_id})

    resp = make_response(redirect(url_for("user_bp.show_user_dashboard")))
    resp.set_cookie(
        "UserToken",
        token,
        httponly=True,
        secure=False,
        samesite="Lax",  # less restrictive for testing
        path="/"
    )
    return resp


# # ---------- LOGOUT ----------
# @user_bp.route("/logout", methods=["GET"])
# def user_logout():
#     """Logs out the admin by clearing session and redirecting to main page."""
#     return render_template("main.html")

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
    return render_template("user/login.html", email=email, password=password)


# ---------- DASHBOARD ----------
@user_bp.route("/", methods=["GET"])
@user_token_required
def show_user_dashboard():
    return render_template("user/dashboard.html")
