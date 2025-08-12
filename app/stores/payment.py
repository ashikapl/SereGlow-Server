from app.utils.supabase_client import supabase


def add_payment_store(data, appointment_id):
    if appointment_id == data.get("appointment_id"):
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
    else:
        return {"error": "Failed to create appointment, service_id and data.get('service_id') not match ."}, 400


def get_payment_store(appointment_id):
    result = supabase.table("Payment").select(
        "*").eq("appointment_id", appointment_id).execute()

    if result.data and len(result.data) > 0:
        return result
    else:
        return {"error": f"No payment found for appointment_id {appointment_id}."}, 404


def update_payment_store(data, appointment_id, payment_id):
    result = supabase.table("Payment").update(
        data).eq("appointment_id", appointment_id).eq("id", payment_id).execute()

    if result.data and len(result.data) > 0:
        return result
    else:
        return {"error": f"Payment with id {appointment_id} and payment_id {payment_id} not found or not updated."}, 404


def delete_payment_store(appointment_id, payment_id):
    result = supabase.table("Payment").delete().eq(
        "appointment_id", appointment_id).eq("id", payment_id).execute()

    if result.data and len(result.data) > 0:
        return result
    else:
        return {"error": f"Payment with id {appointment_id} and service_id {service_id} not found or not updated."}, 404
