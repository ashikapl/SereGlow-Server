class Feedback:
    def __init__(self, id, user_id, service_id, rating, comment):
        self.id = id
        self.user_id = user_id
        self.service_id = service_id
        self.rating = rating
        self.comment = comment

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "service_id": self.service_id,
            "rating": self.rating,
            "comment": self.comment
        }
