from Student import Student
from Subject import Subject

subject1 = Subject("AI", "CS4016", 4, 5)
subject2 = Subject("CA", "CS2014", 2, 5)
subject3 = Subject("AA", "CS4018", 4, 5)
subject4 = Subject("DB", "CS1016", 1, 5)

#so here i pass a list of subjects to my student constructor
raul = Student("Spatariu Raul", 20, "Fagaras", "raulandrei2019@gmail.com", "123124301",
                "superSecretPassword", 2, [subject1, subject2, subject3])

#here I want to be able to see how many credits I have
print(raul.get_total_credits)

