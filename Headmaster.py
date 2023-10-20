from Teacher import Teacher

class Headmaster(Teacher):

    def __init__(self, name: str, age: int, address: str, email: str, id: str, password: str, subjects_taught):
        super().__init__(name, age, address, email, id, password, subjects_taught)


    def __str__(self):
        return super().__str__()