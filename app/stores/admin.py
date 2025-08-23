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


def find_admin_byID(admin_id):
    result = supabase.table("Admin").select(
        "*").eq("id", admin_id).execute()

    if result.data and len(result.data) > 0:
        return result
    else:
        return {"error": f"admin_id {admin_id}, User not found."}, 404
