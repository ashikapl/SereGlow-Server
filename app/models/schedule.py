class Schedule_days:
    def __init__(self, id, day_of_week, is_open):
        self.id = id
        self.day_of_week = day_of_week
        self.is_open = is_open

    def to_dict(self):
        return {
            "id": self.id,
            "day_of_week": self.day_of_week,
            "is_open": self.is_open
        }


class Schedule_time_slot:
    def __init__(self, id, schedule_day_id, start_time, end_time):
        self.id = id
        self.schedule_day_id = schedule_day_id
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            "id": self.id,
            "schedule_day_id": self.schedule_day_id,
            "start_time": self.start_time,
            "end_time": self.end_time
        }
