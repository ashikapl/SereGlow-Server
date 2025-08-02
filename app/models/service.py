class Service:
    def __init__(self, id, name, description, price, duration, image_url):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.duration = duration
        self.image_url = image_url
    
    def to_dict(self):
        return {
            "id":self.id,
            "name":self.name,
            "description":self.description,
            "price":self.price,
            "duration":self.duration,
            "image_url":self.image_url
        }