from app.utils.supabase_client import supabase


def add_appointment_store(data, service_id):
    if service_id == data.get("service_id"):
        result = supabase.table("Appointment").insert({
            "user_id": data.get("user_id"),
            "service_id": data.get("service_id"),
            "appointment_date": data.get("appointment_date"),
            "appointment_time": data.get("appointment_time"),
            "status": data.get("status")
        }).execute()

        if result.data and len(result.data) > 0:
            return result
        else:
            return {"error": "Failed to create appointment."}, 400
    else:
        return {"error": "Failed to create appointment, service_id and data.get('service_id') not match ."}, 400


def get_appointment_store():
    result = supabase.table("Appointment").select(
        "*").execute()

    if result.data and len(result.data) > 0:
        # print("result", result)
        return result
    else:
        return {"error": f"No appointments found!."}, 404


def update_appointment_store(data, service_id, appointment_id):
    result = supabase.table("Appointment").update(
        data).eq("id", appointment_id).eq("service_id", service_id).execute()

    if result.data and len(result.data) > 0:
        return result.data
    else:
        return {"error": f"Appointment with id {appointment_id} and service_id {service_id} not found or not updated."}, 404


def delete_appointment_store(service_id, appointment_id):
    result = supabase.table("Appointment").delete().eq(
        "id", appointment_id).eq("service_id", service_id).execute()

    if result.data and len(result.data) > 0:
        return result.data
    else:
        return {"error": f"Appointment with id {appointment_id} and service_id {service_id} not found or not delete."}, 404


def get_appointment_byUserID(user_id):
    result = supabase.table("Appointment").select(
        "*").eq("user_id", user_id).execute()

    if result.data and len(result.data) > 0:
        # print("result", result)
        return result
    else:
        return {"error": f"No appointments found!."}, 404


def find_user_byID(user_id):
    result = supabase.table("User").select(
        "*").eq("id", user_id).execute()

    if result.data and len(result.data) > 0:
        return result
    else:
        return {"error": f"user_id {user_id}, User not found."}, 404
