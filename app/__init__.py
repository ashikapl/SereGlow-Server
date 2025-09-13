from flask import Flask
from flask_cors import CORS
from config import Config
from app.routes.admin import admin_bp
from app.routes.user import user_bp
from app.routes.service import service_bp
from app.routes.payment import payment_bp
from app.routes.feedback import feedback_bp
from app.routes.appointment import appointment_bp
from app.routes.main import main_bp
from app.routes.schedule import schedule_bp
import os
import stripe
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def create_app():
    app = Flask(__name__, static_folder="../static")
    app.config.from_object(Config)
    app.secret_key = os.getenv("SECRET_KEY")
    stripe.api_key = os.getenv("stripe_api_key")

    # Enable CORS
    CORS(app, supports_credentials=True)

    app.register_blueprint(main_bp, url_prefix="")
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(service_bp, url_prefix="/service")
    app.register_blueprint(appointment_bp, url_prefix="/appointment")
    app.register_blueprint(payment_bp, url_prefix="/payment")
    app.register_blueprint(feedback_bp, url_prefix="/feedback")
    app.register_blueprint(schedule_bp, url_prefix="/schedule")

    return app
