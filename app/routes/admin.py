from flask import jsonify, request, Blueprint, redirect, url_for, render_template, session
from app.services.admin import admin_signup_service, admin_login_service

admin_bp = Blueprint("admin_bp", __name__, template_folder="../../templates")


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
        # return redirect(url_for("admin_bp.admin_signUp"))

    # return jsonify(result.data), 201
    return redirect(url_for("admin_bp.show_admin_login"))


@admin_bp.route("/login", methods=["POST"])
def admin_login():
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()

    result = admin_login_service(data)

    if isinstance(result, tuple):
        return result

    if isinstance(result, dict) and "error" in result:
        return jsonify({"message": "Login Failed!", "error": result["error"]}), 401

    return jsonify({"message": "Login Successfull!"}), 200
    # return render_template("admin/dashboard.html")


@admin_bp.route("/logout", methods=["GET"])
def admin_logout():
    """Logs out the admin by clearing session and redirecting to login page."""
    # session.clear()
    return render_template("main.html")


@admin_bp.route("/signup", methods=["GET"])
def show_admin_signup():
    return render_template("admin/signup.html")


@admin_bp.route("/login", methods=["GET"])
def show_admin_login():
    return render_template("admin/login.html")
