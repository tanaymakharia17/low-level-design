import threading
import time

class SharedCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            local_copy = self.count
            local_copy += 1
            time.sleep(0.1)  # Simulate some work
            self.count = local_copy

class CounterThread(threading.Thread):
    def __init__(self, counter, name):
        super().__init__()
        self.counter = counter
        self.name = name

    def run(self):
        for _ in range(5):
            self.counter.increment()
            print(f"{self.name} incremented count to {self.counter.count}")

# Usage
if __name__ == "__main__":
    counter = SharedCounter()
    t1 = CounterThread(counter, "Thread-1")
    t2 = CounterThread(counter, "Thread-2")

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"Final count: {counter.count}")
