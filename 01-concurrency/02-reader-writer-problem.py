

from abc import ABC, abstractmethod
import threading
import time

class TextFile:

    def __init__(self, name):
        self.__name = name
        self.__content = ""
        self.__lock = threading.Lock()
    
    def read(self):
        # print(f"Reading from {self.__name}: {self.__content}")
        # parallel reads are allowed, so no lock is needed for reading, only block when there is a write
        
    
    def write(self, data):
        with self.__lock:
            print(f"Writing to {self.__name}: {data}")
            self.__content += data
            time.sleep(2)  # Simulate time taken to write
            print(f"Finished writing to {self.__name}")