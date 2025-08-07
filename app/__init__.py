from flask import Flask
from flask_cors import CORS
from config import Config
from app.routes.admin import admin_bp
from app.routes.user import user_bp
from app.routes.services import service_bp
from app.routes.appointment import appointment_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app, supports_credentials=True)

    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(service_bp, url_prefix="/service")
    app.register_blueprint(appointment_bp, url_prefix="/appointment")

    return app
