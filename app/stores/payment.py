from app.utils.supabase_client import supabase


def add_payment_store(data, service_id):
    result = supabase.table("Payment").insert({
        "user_id": data.get("user_id"),
        "service_id": data.get("service_id"),
        "appointment_id": data.get("appointment_id"),
        "amount": data.get("amount"),
        "payment_method": data.get("payment_method"),
        "payment_status": data.get("payment_status"),
        "payment_date": data.get("payment_date"),
        "payment_time": data.get("payment_time")
    }).execute()

    if result:
        return result


def get_payment_store():
    result = supabase.table("Payment").select("*").execute()

    if result:
        return result


def delete_payment_store(appointment_id):
    result = supabase.table("Payment").delete().eq(
        "id", appointment_id).execute()

    if result:
        return result
