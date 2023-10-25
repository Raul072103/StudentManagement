from Person import Person
from Subject import Subject

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
        return super().__str__() + ("id = %s\npassword = %s\nsubjects = {\n%s}" %(self._id, "********", "".join(f"{subject}\n" for subject in self._subjects_taught)) )

if __name__ == '__main__':
    subject11 = Subject("Introduction to Relational Databases", "CS1106", 1, 5)
    subject12 = Subject("Computer Hardware Organisation", "CS1110", 1, 5)
    subject13 = Subject("Systems Organisation", "CS1111", 1, 5)
    subject14 = Subject("Foundations of Computer Science I", "CS1112", 1, 5)
    subject15 = Subject("Foundations of Computer Science II", "CS1113", 1, 5)


    teacher = Teacher("ceva", 20, "asfas", "rafsaf", "123123000", "safasf", [subject11, subject12, subject13])

    print(teacher)