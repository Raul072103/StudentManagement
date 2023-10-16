from Person import Person


class Teacher(Person):

    def __init__(self, name: str, age: int, address: str, email: str, id: str, password: str, subjects_taught):
        super().__init__(name, age, address, email)


    def __str__(self):
        return super().__str__()
