




from abc import ABC, abstractmethod
from dataclasses import dataclass, field

class Student(ABC):
    def __init__(self, name: str, roll_num: str):
        self.__name = name
        self.__roll_num = roll_num
        self.__age = None
        self.__address = None
        self.__email = None
        self.__phone = None
        self.__courses_enrolled = []

    # Properties (Getters)
    @property
    def name(self) -> str:
        return self.__name

    @property
    def roll_number(self) -> str:
        return self.__roll_num

    @property
    def age(self) -> int:
        return self.__age

    @property
    def address(self) -> str:
        return self.__address

    @property
    def email(self) -> str:
        return self.__email

    @property
    def phone(self) -> str:
        return self.__phone

    @property
    def courses_enrolled(self) -> list:
        return list(self.__courses_enrolled)

    # Setters
    @age.setter
    def age(self, age: int):
        self.__age = age

    @address.setter
    def address(self, address: str):
        self.__address = address

    @email.setter
    def email(self, email: str):
        if "@" not in email:
            raise ValueError("Invalid email format.")
        self.__email = email

    @phone.setter
    def phone(self, phone: str):
        self.__phone = phone

    # Method
    def add_course(self, course: str):
        self.__courses_enrolled.append(course)

    def __str__(self):
        return (
            f"Student(name={self.__name}, roll={self.__roll_num}, age={self.__age}, "
            f"address={self.__address}, email={self.__email}, phone={self.__phone}, "
            f"courses={self.__courses_enrolled})"
        )

    
    

class StudentBuilder:
    def __init__(self, name: str, roll_number: str):
        self._name = name
        self._roll_number = roll_number
        self._age = None
        self._address = None
        self._email = None
        self._phone = None
        self._courses = []

    def set_age(self, age: int):
        self._age = age
        return self

    def set_address(self, address: str):
        self._address = address
        return self

    def set_email(self, email: str):
        self._email = email
        return self

    def add_course(self, course: str):
        self._courses.append(course)
        return self

    def build(self):
        student = Student(self._name, self._roll_number)
        if self._age is not None:
            student.age = self._age
        if self._address is not None:
            student.address = self._address
        if self._email is not None:
            student.email = self._email
        for course in self._courses:
            student.add_course(course)
        return student
student = (
    StudentBuilder("Tanay", "CS102")
    .set_age(22)
    .set_address("Mumbai")
    .set_email("tanay@example.com")
    .add_course("LLD")
    .add_course("HLD")
    .build()
)

print(student)