from app.utils.supabase_client import supabase


def add_feedback_store(data, service_id):
    if service_id == int(data.get("service_id")):
        result = supabase.table("Feedback").insert({
            "user_id": data.get("user_id"),
            "service_id": data.get("service_id"),
            "rating": data.get("rating"),
            "comment": data.get("comment"),
        }).execute()

        if result:
            return result
    else:
        return {"error": "Failed to create feedback, service_id and data.get('service_id') not match ."}, 400


# def get_feedback_store(service_id, user_id):
#     result = supabase.table("Feedback").select(
#         "*").eq("service_id", service_id, "user_id", user_id).execute()

#     if result.data and len(result.data) > 0:
#         return result
#     else:
#         return {"error": f"No feedback found for service_id {service_id}."}, 404


def get_feedback_store(service_id, user_id):
    result = (
        supabase.table("Feedback")
        .select("*")
        .eq("service_id", service_id)
        # .eq("user_id", user_id)
        .execute()
    )

    if result.data and len(result.data) > 0:
        return result
    else:
        return {"error": f"No feedback found for service_id {service_id} and user_id {user_id}."}, 404


def update_feedback_store(data, service_id, feedback_id):
    result = supabase.table("Feedback").update(
        data).eq("service_id", service_id).eq("id", feedback_id).execute()

    if result.data and len(result.data) > 0:
        return result
    else:
        return {"error": f"Feedback with id {feedback_id} and service_id {service_id} not found or not updated."}, 404


def delete_feedback_store(service_id, feedback_id):
    result = supabase.table("Feedback").delete().eq(
        "service_id", service_id).eq("id", feedback_id).execute()

    if result.data and len(result.data) > 0:
        return result
    else:
        return {"error": f"Feedback with id {feedback_id} and service_id {service_id} not found or not delete."}, 404


def get_all_feedback_store():
    result = supabase.table("Feedback").select(
        "*").execute()

    if result.data and len(result.data) > 0:
        return result
    else:
        return {"error": f"No feedback found."}, 404
