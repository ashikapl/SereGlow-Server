from app.utils.supabase_client import supabase


def admin_signup_store(data):
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
