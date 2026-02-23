import threading
import time


class BoundedBlockingQueue:
    def __init__(self, capacity: int=4):
        self.__capacity = capacity
        self.__queue = []
        self.__lock = threading.Lock()
        self.__not_empty = threading.Condition(self.__lock)
        self.__not_full = threading.Condition(self.__lock) 

    def enqueue(self, item):
        with self.__lock:
            while len(self.__queue) >= self.__capacity:
                print("Queue is full, waiting for space to enqueue...")
                self.__not_full.wait()
            self.__queue.append(item)
            self.__not_empty.notify()  # Notify one waiting consumer, if any
    
    def dequeue(self):
        with self.__lock:
            while len(self.__queue) == 0:
                print("Queue is empty, waiting for items to be produced...")
                self.__not_empty.wait()
            item = self.__queue.pop(0)
            self.__not_full.notify()  # Notify one waiting producer, if any
            return item

class Producer(threading.Thread):
    def __init__(self, queue: BoundedBlockingQueue, items):
        super().__init__()
        self.queue = queue
        self.items = items

    def run(self):
        for item in self.items:
            print(f"Producing {item}")
            self.queue.enqueue(item)
            time.sleep(1)  # Simulate time taken to process the item

class Consumer(threading.Thread):
    def __init__(self, queue: BoundedBlockingQueue):
        super().__init__(daemon=True) # Daemon thread will exit when main thread exits, even if it's still running
        self.queue = queue

    def run(self):
        while True:
            item = self.queue.dequeue()
            print(f"Consuming {item}")
            time.sleep(1)  # Simulate time taken to process the item        

def producer(queue: BoundedBlockingQueue, items):
    for item in items:
        print(f"Producing {item}")
        queue.enqueue(item)
        time.sleep(3)  # Simulate time taken to process the item

def consumer(queue: BoundedBlockingQueue):
    while True:
        item = queue.dequeue()
        if item is not None:
            print(f"Consuming {item}")
        time.sleep(1)  # Simulate time taken to process the item

if __name__ == "__main__":
    queue = BoundedBlockingQueue(capacity=4)
    items_to_produce = [1, 2, 3, 4, 5]
    
    producer_thread = threading.Thread(target=producer, args=(queue, items_to_produce))
    # dameon thread will exit when main thread exits, so we don't have to wait for it to finish
    consumer_thread = threading.Thread(target=consumer, args=(queue,), daemon=True)

    producer_thread.start()
    consumer_thread.start()

    producer_thread.join()
    # We don't join the consumer thread since it's a daemon thread and will exit when the main thread exits
    # consumer_thread.join() 
    print("Part 1: Producer finished, exiting program.")


    class_producer_thread = Producer(queue, items_to_produce)
    class_consumer_thread = Consumer(queue)
    class_producer_thread.start()
    class_consumer_thread.start()

    class_producer_thread.join()
    # We don't join the consumer thread since it's a daemon thread and will exit when the main thread exits
    # class_consumer_thread.join()
    print("Part 2: Producer finished, exiting program.")
        
