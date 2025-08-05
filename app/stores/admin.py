from app.utils.supabase_client import supabase

def admin_signup_store(data):
    try:
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
        
    except Exception as e:
        error_message = str(e)
        return {"error": error_message}, 500