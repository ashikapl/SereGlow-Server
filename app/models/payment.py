class Payment:
    def __init__(self, id, user_id, service_id, appointment_id, amount, payment_method, payment_status, payment_date, payment_time):
        self.id = id
        self.user_id = user_id
        self.service_id = service_id
        self.appointment_id = appointment_id
        self.amount = amount
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.payment_date = payment_date
        self.payment_time = payment_time

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "service_id": self.service_id,
            "appointment_id": self.appointment_id,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status,
            "payment_date": self.payment_date,
            "payment_time": self.payment_time,
        }
