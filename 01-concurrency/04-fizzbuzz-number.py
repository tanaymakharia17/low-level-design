import time
import threading


class Printer:
    def __init__(self, n):
        self.n = n
        self.lock = threading.Lock()
        self.__number_chance = threading.Condition(self.lock)
        self.__fuzzy_chance = threading.Condition(self.lock)
        self._buzz_chance = threading.Condition(self.lock)
        self.__fizz_chance = threading.Condition(self.lock)
        self.__fizzbuzz_chance = threading.Condition(self.lock)
        self.__current_number = 1

    def print_value_condition(self, number, type):
        if number > self.n:
            return False

        if type == "number":
            return number % 3 != 0 and number % 5 != 0
        elif type == "fizz":
            return number % 3 == 0 and number % 5 != 0
        elif type == "buzz":
            return number % 3 != 0 and number % 5 == 0
        elif type == "fizzbuzz":
            return number % 3 == 0 and number % 5 == 0
        else:
            raise ValueError("Invalid type")

    def print_number(self):
        while self.__current_number <= self.n:
            with self.__number_chance:
                while self.__current_number <= self.n and not self.print_value_condition(self.__current_number, "number"):
                    self.__number_chance.wait()
                print(self.__current_number)
                time.sleep(1)
                self.__current_number += 1
                if self.print_value_condition(self.__current_number, "fizz"):
                    self.__fizz_chance.notify()
                elif self.print_value_condition(self.__current_number, "buzz"):
                    self._buzz_chance.notify() 
                elif self.print_value_condition(self.__current_number, "fizzbuzz"):
                    self.__fizzbuzz_chance.notify()
                elif self.print_value_condition(self.__current_number, "number"):
                    self.__number_chance.notify()
                else:
                    # notify all
                    self.__fizz_chance.notify_all()
                    self._buzz_chance.notify_all()
                    self.__fizzbuzz_chance.notify_all()
                    self.__number_chance.notify_all()
                    break
    
    def print_fizz(self):

        while self.__current_number <= self.n:
            with self.__fizz_chance:
                while not self.print_value_condition(self.__current_number, "fizz"):
                    self.__fizz_chance.wait()
                print("Fizz")
                time.sleep(1)
                self.__current_number += 1
                if self.print_value_condition(self.__current_number, "fizz"):
                    self.__fizz_chance.notify()
                elif self.print_value_condition(self.__current_number, "buzz"):
                    self._buzz_chance.notify() 
                elif self.print_value_condition(self.__current_number, "fizzbuzz"):
                    self.__fizzbuzz_chance.notify()
                elif self.print_value_condition(self.__current_number, "number"):
                    self.__number_chance.notify()
                else:
                    # notify all
                    self.__fizz_chance.notify_all()
                    self._buzz_chance.notify_all()
                    self.__fizzbuzz_chance.notify_all()
                    self.__number_chance.notify_all()
                    break

    def print_buzz(self):
        while self.__current_number <= self.n:
            with self._buzz_chance:
                while not self.print_value_condition(self.__current_number, "buzz"):
                    self._buzz_chance.wait()
                print("Buzz")
                time.sleep(1)
                self.__current_number += 1
                if self.print_value_condition(self.__current_number, "fizz"):
                    self.__fizz_chance.notify()
                elif self.print_value_condition(self.__current_number, "buzz"):
                    self._buzz_chance.notify() 
                elif self.print_value_condition(self.__current_number, "fizzbuzz"):
                    self.__fizzbuzz_chance.notify()
                elif self.print_value_condition(self.__current_number, "number"):
                    self.__number_chance.notify()
                else:
                    # notify all
                    self.__fizz_chance.notify_all()
                    self._buzz_chance.notify_all()
                    self.__fizzbuzz_chance.notify_all()
                    self.__number_chance.notify_all()
                    break

    def print_fizzbuzz(self):
        while self.__current_number <= self.n:
            with self.__fizzbuzz_chance:
                while not self.print_value_condition(self.__current_number, "fizzbuzz"):
                    self.__fizzbuzz_chance.wait()
                print("FizzBuzz")
                time.sleep(1)
                self.__current_number += 1
                if self.print_value_condition(self.__current_number, "fizz"):
                    self.__fizz_chance.notify()
                elif self.print_value_condition(self.__current_number, "buzz"):
                    self._buzz_chance.notify() 
                elif self.print_value_condition(self.__current_number, "fizzbuzz"):
                    self.__fizzbuzz_chance.notify()
                elif self.print_value_condition(self.__current_number, "number"):
                    self.__number_chance.notify()
                else:
                    # notify all
                    self.__fizz_chance.notify_all()
                    self._buzz_chance.notify_all()
                    self.__fizzbuzz_chance.notify_all()
                    self.__number_chance.notify_all()
                    break

if __name__ == "__main__":
    n = 15
    printer = Printer(n)

    number_thread = threading.Thread(target=printer.print_number)
    fizz_thread = threading.Thread(target=printer.print_fizz)
    buzz_thread = threading.Thread(target=printer.print_buzz)
    fizzbuzz_thread = threading.Thread(target=printer.print_fizzbuzz)

    number_thread.start()
    fizz_thread.start()
    buzz_thread.start()
    fizzbuzz_thread.start()

    number_thread.join()
    fizz_thread.join()
    buzz_thread.join()
    fizzbuzz_thread.join()            
                