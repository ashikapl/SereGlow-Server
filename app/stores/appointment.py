from app.utils.supabase_client import supabase


def add_appointment_store(data, service_id):
    result = supabase.table("Appointment").insert({
        "user_id": data.get("user_id"),
        "service_id": data.get("service_id"),
        "appointment_date": data.get("appointment_date"),
        "appointment_time": data.get("appointment_time"),
        "status": data.get("status")
    }).execute()

    if result:
        return result


def get_appointment_store():
    result = supabase.table("Appointment").select("*").execute()

    if result:
        return result


def update_appointment_store(data, appointment_id):
    result = supabase.table("Appointment").update(
        data).eq("id", appointment_id).execute()

    if result:
        return result


def delete_appointment_store(appointment_id):
    result = supabase.table("Appointment").delete().eq(
        "id", appointment_id).execute()

    if result:
        return result
