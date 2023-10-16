from ast import Try

class Person(object):

    def __init__(self, name: str, age: int, address: str, email: str):

        special_characters = "\"!@#$%^&*()-+?_=,<>/"
        if any(c in special_characters for c in name):
            raise TypeError("No special characters are allowed")
        else:
            self._name = name

        if not type(age) is int:
            raise TypeError("Only integers are allows")
        else:
            self._age = age

        special_characters2 = "\"!#$%^&*()-+?_=,<>/"
        if any(c in special_characters2 for c in email):
            raise TypeError("No special characters are allowed except for @")
        else:
            self._email = email

        if any(c in special_characters for c in address):
            raise TypeError("No special characters are allowed")
        else:
            self._address = address

    
    def set_name(self, name):
        self._name = name

    def get_name(self):
        return self._name

    name = property(get_name, set_name)

    def set_age(self, age):
        self._age = age

    def get_age(self):
        return self._age
    
    age = property(get_age, set_age)

    def set_email(self, email):
        self._email = email

    def get_email(self):
        return self._email
    
    email = property(get_email, set_email)

    def set_address(self, address):
        self._address = address

    def get_address(self):
        return self._address
    
    address = property(get_address, set_address)
    
    def __str__(self):
        return ("name = %s\nage = %d\naddress = %s\nemail =  %s\n" %(self._name, self._age, self._address, self._email))

