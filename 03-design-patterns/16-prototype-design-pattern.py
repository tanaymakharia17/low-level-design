"""
When the base variable is very heavy and we want to make many copies of object with minor changes




class Student:
    name = None
    age = None
    __rollNumber = None

    def __init__(self, name, age, rollNumber):
        self.name = name
        self.age = age
        self.__rollNumber = rollNumber



s1 = Student("Tanay", 25, "19ucs122")
# Now I want to make a copy
s2 = Student()
s2.name = s1.name # Wrong as it may be possible name is priivate like roll no.


"""

class Prototype:
    def clone(self): pass


class Student(Prototype):
    name = None
    age = None
    __rollNumber = None

    def __init__(self, name, age, rollNumber):
        self.name = name
        self.age = age
        self.__rollNumber = rollNumber
    
    def clone(self):
        return Student(self.name, self.age, self.__rollNumber)
    
    def __repr__(self):
        return f"{self.name}({self.age}) - {self.__rollNumber}"
    

s1 = Student("Tanay", 25, "19ucs122")
# Now I want to make a copy
s2 = s1.clone()
print(s1)
print(s2)
assert s1 != s2
