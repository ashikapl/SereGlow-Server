from flask import Blueprint, render_template
from app.services.admin import admin_signup_service, admin_login_service

main_bp = Blueprint("main_bp", __name__, template_folder="../../templates")


@main_bp.route('/')
def home():
    return render_template("index.html")
