from app.utils.supabase_client import supabase


def create_signup_store(data):
    result = supabase.table("Admin").insert({
        "firstname": data.get("firstname"),
        "lastname": data.get("lastname"),
        "email": data.get("email"),
        "password": data.get("password"),
        "address": data.get("address"),
        "phone": data.get("phone")
    }).execute()

    if result:
        return result


def get_all_admins_store():
    result = supabase.table("Admin").select("*").execute()

    if result:
        return result
