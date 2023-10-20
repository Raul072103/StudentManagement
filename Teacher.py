from Person import Person


class Teacher(Person):

    def __init__(self, name: str, age: int, address: str, email: str, id: str, password: str, subjects_taught):
        super().__init__(name, age, address, email)
        self._id = id
        self._password = password
        self._subjects_taught = subjects_taught


    def get_id(self):
        return self._id

    def set_id(self, id):
        self._id = id

    id = property(get_id, set_id)

    def get_password(self):
        return self._password
    
    def set_password(self, password):
        self._password = password

    password = property(get_password, set_password)

    def get_subjects_taught(self):
        return self._subjects_taught
    
    def set_subjects_taught(self, subject, index):
        self._subjects_taught[index] = subject

    subjects_taught = property(get_subjects_taught, set_subjects_taught)


    def __str__(self):
        return super().__str__() + ("id = %s\npassword = %s\nsubjects = %s" %(self._id, self._password, ",".join(f"{subject} " for subject in self._subjects_taught)) )

