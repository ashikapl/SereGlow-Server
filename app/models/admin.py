class Admin:
    def __init__(self, id, firstname, lastname, email, password, address, phone):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.address = address
        self.phone = phone

    def to_dict(self):
        return {
            "id":self.id,
            "firstname":self.firstname,
            "lastname":self.lastname,
            "email":self.email,
            "password":self.password,
            "address":self.address,
            "phone":self.phone
        }