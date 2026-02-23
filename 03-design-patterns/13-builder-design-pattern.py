"""
Examples - StringBuilder in java
Builder vs Decorator

Suppose i have to create an object of student and it have many fields in the constructors like name, age, city, mom_name, -----

Now this will ne huge to this is solve by builder design pattern.
Build an oject step by step


"""

class Student:
    def __init__(self, name, age, grade, subjects, address):
        self.name = name
        self.age = age
        self.grade = grade
        self.subjects = subjects
        self.address = address

    def __str__(self):
        return (f"Student(Name: {self.name}, Age: {self.age}, "
                f"Grade: {self.grade}, Subjects: {self.subjects}, "
                f"Address: {self.address})")

class StudentBuilder:
    def __init__(self):
        self._name = None
        self._age = None
        self._grade = None
        self._subjects = []
        self._address = None

    def set_name(self, name):
        self._name = name
        return self

    def set_age(self, age):
        self._age = age
        return self

    def set_grade(self, grade):
        self._grade = grade
        return self

    def add_subject(self, subject):
        self._subjects.append(subject)
        return self

    def set_address(self, address):
        self._address = address
        return self

    def build(self):
        return Student(self._name, self._age, self._grade, self._subjects, self._address)

# Usage example:
if __name__ == "__main__":
    student = (StudentBuilder()
               .set_name("John Doe")
               .set_age(16)
               .set_grade("10th")
               .add_subject("Mathematics")
               .add_subject("Science")
               .set_address("123 Main Street")
               .build())
    print(student)