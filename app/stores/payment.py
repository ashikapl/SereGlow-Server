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
        }).execute()

        if result:
            return result
    else:
        return {"error": "Failed to create appointment, appointment_id and data.get('appointment_id') not match ."}, 400


def get_payment_store():
    result = supabase.table("Payment").select(
        "*").execute()

    if result.data and len(result.data) > 0:
        return result
    else:
        return {"error": f"No payment found!."}, 404


def get_user_payment_store(user_id):
    result = supabase.table("Payment").select(
        "*").eq("user_id", user_id).execute()

    if result.data and len(result.data) > 0:
        return result
    return []


def update_payment_status_store(payment_id, data):
    result = supabase.table("Payment").update(
        data).eq("id", payment_id).execute()
    if result.data and len(result.data) > 0:
        return result
    else:
        return {"error": f"Payment with id {payment_id} not found or not updated."}, 404


def delete_payment_store(appointment_id, payment_id):
    result = supabase.table("Payment").delete().eq(
        "appointment_id", appointment_id).eq("id", payment_id).execute()

    if result.data and len(result.data) > 0:
        return result
    else:
        return {"error": f"Payment with id {appointment_id} and payment_id {payment_id} not found or not delete."}, 404


# def get_payment_byUserID(user_id):
#     result = supabase.table("Payment").select(
#         "*").eq("user_id", user_id).execute()

#     if result.data and len(result.data) > 0:
#         # print("result", result)
#         return result
#     else:
#         return {"error": f"No appointments found!."}, 404

def get_payment_byUserID(user_id):
    result = supabase.table("Payment").select(
        "*").eq("user_id", user_id).execute()
    return result.data or []   # always return a list


def find_user_byID(user_id):
    result = supabase.table("User").select(
        "*").eq("id", user_id).execute()

    if result.data and len(result.data) > 0:
        return result
    else:
        return {"error": f"user_id {user_id}, User not found."}, 404
