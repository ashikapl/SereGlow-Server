class User:
    def __init__(self, id, firstname, lastname, username, email, password, address, phone):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.email = email
        self.password = password
        self.address = address
        self.phone = phone

    def to_dict(self):
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "username": self.username,
            "email": self.email,
            "password": self.password,
            "address": self.address,
            "phone": self.phone
        }
