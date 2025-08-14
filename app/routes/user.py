from flask import jsonify, request, Blueprint, redirect, url_for, render_template, session
from app.services.user import user_signup_service, user_login_service

user_bp = Blueprint("user_bp", __name__, template_folder="../../templates")


@user_bp.route('/register', methods=['POST'])
def user_signUp():
    # data = request.get_json()
    data = request.form.to_dict()

    result = user_signup_service(data)

    print("routers result: ", result)

    if isinstance(result, tuple):
        return result

    # return jsonify(result.data), 201
    return render_template("user/dashboard.html")


@user_bp.route("/login", methods=["POST"])
def user_login():
    # data = request.get_json()
    data = request.form.to_dict()

    result = user_login_service(data)

    if "error" in result:
        return jsonify({"message": "Login Failed!"}), 404

    # return jsonify({"message": "Login Successfull!"})
    return render_template("user/dashboard.html")


@user_bp.route("/logout", methods=["GET"])
def user_logout():
    """Logs out the admin by clearing session and redirecting to login page."""
    # session.clear()
    return render_template("main.html")
