class Appointment:
    def __init__(self, id, user_id, service_id, appointment_date, appointment_time, status, created_at):
        self.id = id
        self.user_id = user_id
        self.service_id = service_id
        self.appointment_date = appointment_date
        self.appointment_time = appointment_time
        self.status = status
        self.created_at = created_at

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "service_id": self.service_id,
            "appointment_date": str(self.appointment_date),
            "appointment_time": str(self.appointment_time),
            "status": self.status,
            "created_at": str(self.created_at)
        }
