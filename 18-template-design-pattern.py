

"""
I want some classes to follow a particular pattern, like sending money, 
# so we just override the steps not thte final order of steps

"""
from abc import ABC, abstractmethod
from typing import final


class PaymentProcessor(ABC):

    def process_payment(self):
        self.authenticate_user()
        self.validate_payment_details()
        self.make_payment()
        self.send_confirmation()

    @abstractmethod
    def authenticate_user(self):
        pass

    @abstractmethod
    def validate_payment_details(self):
        pass

    @abstractmethod
    def make_payment(self):
        pass
    
    @final
    def send_confirmation(self):
        print("Sending payment confirmation email.\n")


class BadUPIPayment(PaymentProcessor):
    def authenticate_user(self): pass
    def validate_payment_details(self): pass
    def make_payment(self): pass

    def send_confirmation(self): 
        print("Hacked confirmation")




tmp = BadUPIPayment()