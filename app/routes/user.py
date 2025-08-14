from flask import (
    jsonify, request, Blueprint, redirect, url_for, render_template,
    make_response, json
)
from app.services.user import user_signup_service, user_login_service
from app.utils.user_validator import generate_token

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

    if isinstance(result, dict) and "error" in result:
        return jsonify({"message": "Login Failed!", "error": result["error"]}), 401
    
    data_dict = json.loads(result[0].data.decode('utf-8'))
    # user_id = data_dict['user']['id'] 
    user_id = data_dict.get('user', {}).get('id')

    token = generate_token({"user_id": user_id})

    resp = make_response(redirect(url_for("user_bp.show_user_dashboard")))
    resp.set_cookie(
        "authToken", 
        token,
        httponly=True,
        secure=False,   # Change to True for HTTPS
        samesite="Strict"
    )
    return resp


# ---------- LOGOUT ----------
@user_bp.route("/logout", methods=["GET"])
def user_logout():
    """Logs out the admin by clearing session and redirecting to main page."""
    return render_template("main.html")


# ---------- SIGNUP (GET) ----------
@user_bp.route("/signup", methods=["GET"])
def show_user_signup():
    return render_template("user/signup.html")


# ---------- LOGIN (GET) ----------
@user_bp.route("/getlogin", methods=["GET"])
def show_user_login():
    email = request.args.get("email", "")
    password = request.args.get("password", "")
    return render_template("user/login.html", email=email, password=password)


# ---------- DASHBOARD ----------
@user_bp.route("/", methods=["GET"])
def show_user_dashboard():
    return render_template("user/dashboard.html")
