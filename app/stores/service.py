from app.utils.supabase_client import supabase


def add_service_store(data):
    result = supabase.table("Service").insert({
        "name": data.get("name"),
        "description": data.get("description"),
        "price": data.get("price"),
        "duration": data.get("duration"),
        "image_url": data.get("image_url")
    }).execute()

    if result:
        return result


def get_service_store():
    result = supabase.table("Service").select("*").execute()

    if result:
        return result


def update_service_store(data, service_id):
    result = supabase.from_("Service").update(
        data).eq("id", service_id).execute()

    # print("res", result)

    if result.data:
        return result
    else:
        return {"error": f"Service with id {service_id} not found"}, 404


def delete_service_store(service_id):
    result = supabase.table("Service").delete().eq("id", service_id).execute()

    if result.data and len(result.data) > 0:
        return result
    else:
        return {"error": f"Service with id {service_id} not found"}, 404


def get_service_byId(service_id):
    result = supabase.table("Service").select(
        "*").eq("id", service_id).execute()

    if result:
        return result
