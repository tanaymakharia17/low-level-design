
import time
import threading

class AlternateEvenOddPrinter:
    def __init__(self, n):
        self.__n = n
        self.__lock = threading.Lock()
        self.__turn = 'odd'  # Start with even
        self.__allow_even_condition = threading.Condition(self.__lock)
        self.__allow_odd_condition = threading.Condition(self.__lock)

    
    def print_even(self):
        for i in range(2, self.__n + 1, 2):
            with self.__lock:

                while self.__turn != 'even':
                    self.__allow_even_condition.wait()
                print(i)
                time.sleep(1)
                self.__turn = 'odd'
                self.__allow_odd_condition.notify()
        

    def print_odd(self):
        for i in range(1, self.__n + 1, 2):
            with self.__lock:

                while self.__turn != 'odd':
                    self.__allow_odd_condition.wait()
                print(i)
                time.sleep(1)
                self.__turn = 'even'
                self.__allow_even_condition.notify()
    

if __name__ == "__main__":
    n = 13

    printer = AlternateEvenOddPrinter(n)
    even_thread = threading.Thread(target=printer.print_even)
    odd_thread = threading.Thread(target=printer.print_odd)

    even_thread.start()
    odd_thread.start()  
    even_thread.join()
    odd_thread.join()