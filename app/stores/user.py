from app.utils.supabase_client import supabase
from app.utils.helpers import generate_username

def create_signup_store(data):
    result = supabase.table("User").insert({
            "firstname": data.get("firstname"),
            "lastname": data.get("lastname"),
            "username": generate_username(data.get("firstname"), data.get("lastname")),
            "email": data.get("email"),
            "password": data.get("password"),
            "address": data.get("address"),
            "phone": data.get("phone")
    }).execute()

    if result:
        return result


def get_all_users_store():
    result = supabase.table("User").select("*").execute()

    if result:
        return result
