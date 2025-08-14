from flask import jsonify, request, Blueprint, redirect, url_for, render_template, session
from app.services.user import user_signup_service, user_login_service

user_bp = Blueprint("user_bp", __name__, template_folder="../../templates")


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
        # return redirect(url_for("user_bp.user_signUp"))

    # return jsonify(result.data), 201
    return redirect(url_for("user_bp.show_user_login"))


@user_bp.route("/login", methods=["POST"])
def user_login():
    # data = request.get_json()
    data = request.form.to_dict()

    result = user_login_service(data)

    if isinstance(result, tuple):
        return result

    if isinstance(result, dict) and "error" in result:
        return jsonify({"message": "Login Failed!", "error": result["error"]}), 401

    return jsonify({"message": "Login Successfull!"})
    # return render_template("user/dashboard.html")


@user_bp.route("/logout", methods=["GET"])
def user_logout():
    """Logs out the admin by clearing session and redirecting to login page."""
    # session.clear()
    return render_template("main.html")


@user_bp.route("/signup", methods=["GET"])
def show_user_signup():
    return render_template("user/signup.html")


@user_bp.route("/login", methods=["GET"])
def show_user_login():
    return render_template("user/login.html")
