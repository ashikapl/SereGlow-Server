class Payment:
    def __init__(self, id, user_id, service_id, appointment_id, amount, payment_method, payment_status, payment_created_at):
        self.id = id
        self.user_id = user_id
        self.service_id = service_id
        self.appointment_id = appointment_id
        self.amount = amount
        self.payment_method = payment_method
        self.payment_status = payment_status
        self.payment_created_at = payment_created_at

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "service_id": self.service_id,
            "appointment_id": self.appointment_id,
            "amount": self.amount,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status,
            "payment_created_at": self.payment_created_at,
        }
