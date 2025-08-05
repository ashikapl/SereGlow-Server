from app.utils.supabase_client import supabase


def create_service_store(data):
    result = supabase.table("Service").insert({
        "name": data.get("name"),
        "description": data.get("description"),
        "price": data.get("price"),
        "duration": data.get("duration"),
        "image_url": data.get("image_url")
    }).execute()

    if result:
        return result


def read_service_store():
    result = supabase.table("Service").select("*").execute()

    if result:
        return result


def update_service_store(data, service_id):
    result = supabase.table("Service").update(
        data).eq("id", service_id).execute()

    if result:
        return result


def delete_service_store(service_id):
    result = supabase.table("Service").delete().eq("id", service_id).execute()

    if result:
        return result
