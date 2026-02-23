import threading
import time

class WorkerThread(threading.Thread):
    def __init__(self, name, time=1):
        super().__init__()
        self.name = name
        self.time = time

    def run(self):
        for i in range(5):
            print(f"{self.name} is working on iteration {i}")
            time.sleep(self.time)

# Usage
if __name__ == "__main__":
    t1 = WorkerThread("Thread-1")
    t2 = WorkerThread("Thread-2", 2)

    t1.start()
    t2.start()
    t2.join()
    t1.join()
    print("Thread 1 completed")
    # t2.join()

    print("Both threads completed.")
