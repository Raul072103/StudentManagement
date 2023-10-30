class Subject(object):

    def __init__(self, name: str, code: str, year: int, credits_worth: int):
        self._name = name
        self._code = code
        self._year = year
        self._credits_worth = credits_worth

    def get_credits_worth(self):
        return self._credits_worth
    
    def set_credits_worth(self, credits_worth):
        self._credits_worth = credits_worth

    credits_worth = property(get_credits_worth, set_credits_worth)   

    def get_name(self):
        return self._name 
    
    def set_name(self, name):
        self._name = name

    name = property(get_name, set_name)

    def get_code(self):
        return self._code

    def set_code(self, code):
        self._code = code

    code = property(get_code, set_code)

    def get_year(self):
        return self._year

    def set_year(self, year):
        self._year = year

    year = property(get_year, set_year)

    def __str__(self):
        return (" subject_name = %s code = %s year = %d credits = %d" %(self._name, self._code, self._year, self._credits_worth))
    
        

