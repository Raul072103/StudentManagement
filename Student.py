from Person import Person
from Subject import Subject


class Student(Person):

    def __init__(self, name: str, age: int, address: str, email: str,
                  id: str, password: str, current_year: int, subject_mark: dict[str, float]):
        super().__init__(name, age, address, email)
        self._id = id
        self._password = password
        self._current_year = current_year
        self._subject_mark = subject_mark

    #student_id
    def get_id(self):
        return self._id
    
    def set_id(self, id):
        self._id = id

    id = property(get_id, set_id)

    #current_year
    def get_currentYear(self):
        return self._current_year

    def set_currentYear(self, current_year):  
        self._current_year = current_year

    current_year = property(get_currentYear, set_currentYear)

    #password
    def get_password(self):
        return self._password

    def set_password(self, password):
        self._password = password

    password = property(get_password, set_password)

    #method for getting the total credits
    def get_total_credits(self):
       total_credits = 0
       i = 0
       for subject in self._subject_mark:
           if  self._subject_mark[subject] > 5.0:
                total_credits = total_credits + 5

       return total_credits    
    
    #subjects
    def subjects(self):
        subject_list = []
        for i in self._subject_mark:
            subject_list.append(i)
        return subject_list
    
    #subject_mark dicitonary
    def get_subject_mark(self):
        return self._subject_mark
    
    #marks_list
    def marks_list(self):
        marks_list = []
        for i in self._subject_mark:
            marks_list.append(self._subject_mark[i])
        return marks_list
    
    def set_subject_mark(self, new_dict):
        if isinstance(new_dict, dict):
            self._subject_mark = new_dict
        else:
            raise ValueError("Input must be a dictionary")
        
    subject_mark = property(get_subject_mark, set_subject_mark)


    def __str__(self):
        return super().__str__() + ("id = %s\npassword = %s\ncurrent_year = %d\n" %(self._id, self._password, self._current_year) ) + str(self._subject_mark)


if __name__ == '__main__':
    student1 = Student("Spatariu Raul", 20, "Fagaras", "raulandrei2019@gmail.com", "200000001",
                "superSecretPassword", 2, {"cs11": 0.0, "cs22": 0.0})
    print(student1.subjects())
 