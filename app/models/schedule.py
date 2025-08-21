class Schedule:
    def __init__(self, id, day_of_week, is_open, start_time, end_time):
        self.id = id
        self.day_of_week = day_of_week
        self.is_open = is_open
        self.start_time = start_time
        self.end_time = end_time

    def to_dict(self):
        return {
            "id": self.id,
            "day_of_week": self.day_of_week,
            "is_open": self.is_open,
            "start_time": self.start_time,
            "end_time": self.end_time,
        }
