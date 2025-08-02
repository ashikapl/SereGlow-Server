import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    # Flask settings
    DEBUG = False
    TESTING = False

    # Supabase credentials
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_APIKEY")
    # SUPABASE_DB_URI = os.getenv("SUPABASE_DB_URI")

    # SQLAlchemy
    # SQLALCHEMY_DATABASE_URI = SUPABASE_DB_URI
    # SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Supabase auth headers (optional)
    SUPABASE_HEADERS = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
