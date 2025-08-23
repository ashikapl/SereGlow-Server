from app.utils.supabase_client import supabase


def add_schedule_store(data):
    day_of_week = data.get("day_of_week")
    is_open = data.get("is_open")

    # Check if day already exists
    existing_day = supabase.table("Schedule_days").select(
        "*").eq("day_of_week", day_of_week).execute()

    if existing_day.data:
        # Update existing day
        day_id = existing_day.data[0]["id"]
        supabase.table("Schedule_days").update({
            "is_open": is_open
        }).eq("id", day_id).execute()
    else:
        # Insert new day
        schedule_day = supabase.table("Schedule_days").insert({
            "day_of_week": day_of_week,
            "is_open": is_open,
        }).execute()

        if not schedule_day.data:
            return {"error": "Failed to create schedule day."}, 400

        day_id = schedule_day.data[0]["id"]

    # Insert multiple time slots
    slots = data.get("slots", [])
    inserted_slots = []
    for slot in slots:
        schedule_time_slot = supabase.table("Schedule_time_slot").insert({
            "schedule_day_id": day_id,
            "start_time": slot.get("start_time"),
            "end_time": slot.get("end_time")
        }).execute()

        if schedule_time_slot.data:
            inserted_slots.append(schedule_time_slot.data[0])

    return {
        "day_id": day_id,
        "day_of_week": day_of_week,
        "is_open": is_open,
        "slots": inserted_slots
    }


def get_schedule_store():
    Schedule_days = supabase.table("Schedule_days").select(
        "*").execute()
    Schedule_time_slot = supabase.table("Schedule_time_slot").select(
        "*").execute()

    if (Schedule_days.data and len(Schedule_days.data) > 0) and (Schedule_time_slot.data and len(Schedule_time_slot.data) > 0):
        return [Schedule_days, Schedule_time_slot]
    else:
        return {"error": f"No schedule found!."}, 404

# def get_schedule_store():
#     Schedule_days = supabase.table("Schedule_days").select(
#         "*").execute()
#     Schedule_time_slot = supabase.table("Schedule_time_slot").select(
#         "*").execute()

#     if (Schedule_days.data and len(Schedule_days.data) > 0) and (Schedule_time_slot.data and len(Schedule_time_slot.data) > 0):
#         return [Schedule_days, Schedule_time_slot]
#     else:
#         return {"error": f"No schedule found!."}, 404


def update_schedule_store(data, schedule_day_id):
    day_update = supabase.table("Schedule_days").update({
        "day_of_week": data.get("day_of_week"),
        "is_open": data.get("is_open")
    }).eq("id", schedule_day_id).execute()

    slot_update = supabase.table("Schedule_time_slot").update({
        "start_time": data.get("start_time"),
        "end_time": data.get("end_time")
    }).eq("schedule_day_id", schedule_day_id).execute()

    if day_update.data or slot_update.data:
        return {"day": day_update.data, "slot": slot_update.data}
    else:
        return {"error": f"Schedule with id {schedule_day_id} not updated."}, 404


def delete_schedule_store(schedule_day_id):
    # delete slots first (foreign key)
    slots = supabase.table("Schedule_time_slot").delete().eq(
        "schedule_day_id", schedule_day_id).execute()
    day = supabase.table("Schedule_days").delete().eq(
        "id", schedule_day_id).execute()

    if day.data:
        return {"day": day.data, "slots": slots.data}
    else:
        return {"error": f"Schedule with id {schedule_day_id} not deleted."}, 404
