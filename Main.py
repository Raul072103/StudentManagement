from Student import Student
from Subject import Subject
from Teacher import Teacher
from Headmaster import Headmaster

subject1 = Subject("AI", "CS4016", 4, 5)
subject2 = Subject("CA", "CS2014", 2, 5)
subject3 = Subject("AA", "CS4018", 4, 5)
subject4 = Subject("DB", "CS1016", 1, 5)

#so here i pass a list of subjects to my student constructor
raul = Student("Spatariu Raul", 20, "Fagaras", "raulandrei2019@gmail.com", "123124301",
                "superSecretPassword", 2, [subject1, subject2, subject3], [5.6, 7.8, 9.0])

derek = Teacher("Derek Bridge", 50, "Cork", "derekbridge@ucc.ie", "100101001", "TheFinalBoss", [subject1, subject2, subject3])

racu = Headmaster("Maria Racu", 45, "Fagaras", "maria.racu@ucc.ie", "100000001", "MariaRacu", [subject1, subject2])

print(racu)


