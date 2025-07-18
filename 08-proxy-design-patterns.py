"""
Create proxies between client and real object for extra work like validation, cache checking, etc.

"""
from abc import ABC, abstractmethod

class EmployeeTable(ABC):

    @abstractmethod
    def create(self):
        pass
    
    @abstractmethod
    def remove(self):
        pass
    


class EmployeeTableIndia(EmployeeTable):

    def create(self):
        print(f"New employee is created")
    
    def remove(self):
        print("Employee removed")


class EmployeeProxyValidation(EmployeeTable):
    employee_obj = None

    def __init__(self, employee_obj):
        self.employee_obj = employee_obj

    
    def create(self):
        print("This is passed through proxy Validation")
        self.employee_obj.create()
    
    def remove(self):
        print("This is passed through proxy Validation")
        self.employee_obj.remove()
    
class EmployeeProxyCache(EmployeeTable):
    employee_obj = None

    def __init__(self, employee_obj):
        self.employee_obj = employee_obj

    
    def create(self):
        print("This is passed through proxy Cache")
        self.employee_obj.create()
    
    def remove(self):
        print("This is passed through proxy Cache")
        self.employee_obj.remove()


et = EmployeeTableIndia()
epc = EmployeeProxyCache(et)
epv = EmployeeProxyValidation(epc)

epv.create()
epv.remove()
