from PrintOptionsInterface import PrintOptionsInterface
from Teacher import Teacher

class Headmaster(Teacher, PrintOptionsInterface):

    def __init__(self, name: str, age: int, address: str, email: str, id: str, password: str, subjects_taught):
        super().__init__(name, age, address, email, id, password, subjects_taught)

    #here i override the method from the interface
    def print_options(self):
        print("1. View all students")
        print("2. View information about a student")
        print("3. Mark your students")
        print("4. Delete a student")
        print("5. Insert a student")
        print("6. View all teachers")
        print("7. View information about a teacher")
        print("8. Delete a teacher")
        print("9. Insert a teacher")
        print("10. View all subjects")
        print("11. Delete a subject")
        print("12. Insert a subject")
        print("13. Exit")
     
    def __str__(self):
        return super().__str__()