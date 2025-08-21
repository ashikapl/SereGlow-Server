from app.utils.supabase_client import supabase


def add_schedule_store(data):
    result = supabase.table("Schedule").insert({
        "day_of_week": data.get("day_of_week"),
        "is_open": data.get("is_open"),
        "start_time": data.get("start_time"),
        "end_time": data.get("end_time")
    }).execute()

    if result.data and len(result.data) > 0:
        return result
    else:
        return {"error": "Failed to create schedule."}, 400


def get_schedule_store():
    Schedule_days = supabase.table("Schedule_days").select(
        "*").execute()
    Schedule_time_slot = supabase.table("Schedule_time_slot").select(
        "*").execute()

    if (Schedule_days.data and len(Schedule_days.data) > 0) and (Schedule_time_slot.data and len(Schedule_time_slot.data) > 0):
        return [Schedule_days, Schedule_time_slot]
    else:
        return {"error": f"No schedule found!."}, 404


def update_schedule_store(data, schedule_id):
    result = supabase.table("Schedule").update(
        data).eq("id", schedule_id).execute()

    if result.data and len(result.data) > 0:
        return result.data
    else:
        return {"error": f"Schedule with id {schedule_id} not updated."}, 404


def delete_schedule_store(schedule_id):
    result = supabase.table("Schedule").delete().eq(
        "id", schedule_id).execute()

    if result.data and len(result.data) > 0:
        return result.data
    else:
        return {"error": f"Schedule with id {schedule_id} not delete."}, 404
