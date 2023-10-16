from locale import currency
from re import sub
from Person import Person
from Subject import Subject


class Student(Person):

    def __init__(self, name: str, age: int, address: str, email: str,
                  id: str, password: str, current_year: int, subjects: Subject):
        super().__init__(name, age, address, email)
        self._id = id
        self._password = password
        self._current_year = current_year
        self._subjects = subjects
        self._marks_list = [0] * len(self._subjects)


    def get_id(self):
        return self._id
    
    def set_id(self, id):
        self._id = id

    id = property(get_id, set_id)

    def get_currentYear(self):
        return self._current_year

    def set_currentYear(self, current_year):  
        self._current_year = current_year

    current_year = property(get_currentYear, set_currentYear)

    def get_subjects(self):
        temp_list = []
        for i in self._subjects:
            temp_list.append(i)

        return temp_list     
    
    def set_subjects(self, subjects):
        for i in subjects:
            self._subjects.append(i)

    subjects = property(get_subjects, set_subjects)

    def get_password(self):
        return self._password

    def set_password(self, password):
        self._password = password

    password = property(get_password, set_password)

    def get_total_credits(self):
       total_credits = 0

       for i in range(0, len(self._marks_list)):
           if self._marks_list[i] >= 5:
            total_credits = total_credits + self._subject[i].get_credits_worth

       return total_credits    
           

    def get_marks_list(self):
        return self._marks_list

    def set_marks_list(self, mark, index):
        self._marks_list[index]  = mark

    marks_list = property(get_marks_list, set_marks_list) 

    def __str__(self):
        return super().__str__() + ("id = %s\npassword = %s\ncurrent_year = %d\nsubjects = %s" %(self._id, self._password, self._current_year, ",".join(f"{subject} " for subject in self._subjects)) )


