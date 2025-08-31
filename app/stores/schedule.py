from app.utils.supabase_client import supabase


def add_schedule_store(data, id):
    day_of_week = data.get("day_of_week")
    is_open = data.get("is_open")

    # --- Step 1: Find or create schedule day ---
    existing_day = supabase.table("Schedule_days").select(
        "*"
    ).eq("day_of_week", day_of_week).execute()

    if existing_day.data:
        day_id = existing_day.data[0]["id"]
        supabase.table("Schedule_days").update(
            {"is_open": is_open}
        ).eq("id", day_id).execute()
    else:
        schedule_day = supabase.table("Schedule_days").insert({
            "day_of_week": day_of_week,
            "is_open": is_open,
        }).execute()

        if not schedule_day.data:
            return {"error": "Failed to create schedule day."}, 400

        day_id = schedule_day.data[0]["id"]

    # --- Step 2: Replace slots for this day ---
    supabase.table("Schedule_time_slot").delete().eq(
        "schedule_day_id", day_id).execute()

    slots = data.get("slots", [])
    inserted_slots = []

    if is_open:
        for slot in slots:
            schedule_time_slot = supabase.table("Schedule_time_slot").insert({
                "schedule_day_id": day_id,
                "start_time": slot.get("start_time"),
                "end_time": slot.get("end_time")
            }).execute()

            if schedule_time_slot.data:
                inserted_slots.append(schedule_time_slot.data[0])

    # --- Step 3: Always return JSON-compatible dict ---
    return {
        "day_id": day_id,
        "day_of_week": day_of_week,
        "is_open": is_open,
        "slots": inserted_slots
    }


def get_schedule_store():
    schedules = supabase.table("Schedule_days").select(
        "id, day_of_week, is_open, Schedule_time_slot(id, start_time, end_time)"
    ).order("id", desc=False).execute()

    if schedules.data:
        return schedules.data
    else:
        return {"error": "No schedule found!"}, 404


def update_schedule_store(data, schedule_day_id):
    # Update day info
    day_update = supabase.table("Schedule_days").update({
        "day_of_week": data.get("day_of_week"),
        "is_open": data.get("is_open")
    }).eq("id", schedule_day_id).execute()

    slot_update = None
    slot_id = data.get("slot_id")
    if slot_id:
        # Update only the given slot
        slot_update = supabase.table("Schedule_time_slot").update({
            "start_time": data.get("start_time"),
            "end_time": data.get("end_time")
        }).eq("id", slot_id).execute()

    if day_update.data or (slot_update and slot_update.data):
        return {"day": day_update.data, "slot": slot_update.data if slot_update else None}
    else:
        return {"error": f"Schedule with id {schedule_day_id} not updated."}, 404


def delete_schedule_store(slot_id):
    # 1. Get the slot before deleting
    slot = supabase.table("Schedule_time_slot").select(
        "*").eq("id", slot_id).execute()

    if not slot.data:
        return {"error": f"Slot with id {slot_id} not found."}, 404

    deleted_slot = slot.data[0]
    schedule_day_id = deleted_slot["schedule_day_id"]

    # 2. Delete the slot
    supabase.table("Schedule_time_slot").delete().eq("id", slot_id).execute()

    # 3. Check if that day still has slots
    remaining_slots = supabase.table("Schedule_time_slot").select(
        "*").eq("schedule_day_id", schedule_day_id).execute()

    if not remaining_slots.data:
        supabase.table("Schedule_days").delete().eq(
            "id", schedule_day_id).execute()

    return {"deleted_slot": deleted_slot}


def reset_time_slot_sequence():
    supabase.rpc("exec_sql", {
        "sql": 'ALTER SEQUENCE Schedule_time_slot_id_seq RESTART WITH 1;'
    }).execute()
