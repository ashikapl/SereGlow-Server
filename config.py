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
    SUPABASE_APIKEY = os.getenv("SUPABASE_APIKEY")

    # Supabase auth headers (optional)
    SUPABASE_HEADERS = {
        "apikey": SUPABASE_APIKEY,
        "Authorization": f"Bearer {SUPABASE_APIKEY}",
        "Content-Type": "application/json"
    }
