from app.utils.supabase_client import supabase

<<<<<<< HEAD
def add_service_store(data):
=======

def create_service_store(data):
>>>>>>> 4ab05fdd7db5d3325d666c9df532cc0700d60adb
    result = supabase.table("Service").insert({
        "name": data.get("name"),
        "description": data.get("description"),
        "price": data.get("price"),
        "duration": data.get("duration"),
        "image_url": data.get("image_url")
    }).execute()

    if result:
        return result

<<<<<<< HEAD
def get_service_store():
=======

def read_service_store():
>>>>>>> 4ab05fdd7db5d3325d666c9df532cc0700d60adb
    result = supabase.table("Service").select("*").execute()

    # print("result", result)

    if result:
        return result

def update_service_store(data, service_id):
    result = supabase.table("Service").update(
        data).eq("id", service_id).execute()

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
