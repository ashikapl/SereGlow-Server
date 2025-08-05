from app.utils.supabase_client import supabase


def add_feedback_store(data, service_id):
    result = supabase.table("Feedback").insert({
        "user_id": data.get("user_id"),
        "service_id": data.get("service_id"),
        "rating": data.get("rating"),
        "comment": data.get("comment"),
    }).execute()

    if result:
        return result


def get_feedback_store():
    result = supabase.table("Feedback").select("*").execute()

    if result:
        return result


def update_feedback_store(data, appointment_id):
    result = supabase.table("Feedback").update(
        data).eq("id", appointment_id).execute()

    if result:
        return result


def delete_feedback_store(appointment_id):
    result = supabase.table("Feedback").delete().eq(
        "id", appointment_id).execute()

    if result:
        return result
