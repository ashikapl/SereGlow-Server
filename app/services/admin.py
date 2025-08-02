from flask import jsonify
from app.extensions.supabase_client import supabase

def create_signup_service(data):
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

        # Detect UNIQUE constraint violation (email already exists)
        if 'duplicate key value violates unique constraint' in error_message and 'admin_email_key' in error_message:
            return {"error": "Email already exists"}, 409  # HTTP 409 Conflict

        return {"error": error_message}, 500

def get_all_admins_Service():
    try:
        result = supabase.table("Admin").select("*").execute()

        if result:
            return result
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500