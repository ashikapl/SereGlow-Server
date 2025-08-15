import jwt
import datetime
from app.utils.supabase_client import supabase
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def admin_generate_token(admin_id):
    payload = {
        'admin_id': admin_id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, os.getenv(
        "SUPABASE_APIKEY"), algorithm='HS256')
    return token


def user_generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, os.getenv(
        "SUPABASE_APIKEY"), algorithm='HS256')
    return token


def decode_token(token):
    try:
        payload = jwt.decode(token, os.getenv(
            "SUPABASE_APIKEY"), algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def user_validator(email, password, table_name):
    result = supabase.table(table_name).select(
        "*").eq("email", email).execute()

    user = result.data

    if not user or len(user) == 0:
        return False  # No user found

    # Compare passwords (you should use hashing like bcrypt in real apps)
    if user[0]['password'] != password:
        return False  # Wrong password

    return user[0]
