from flask import Flask
from flask_cors import CORS
from supabase import create_client, Client
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app, supports_credentials=True)

    return app

# Initialize Supabase client globally
supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
