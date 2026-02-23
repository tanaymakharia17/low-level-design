"""

Only 1 instance of a class

"""



class Singleton:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None: # Problem in threading
            print("Creating new instance")
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

# Example usage
if __name__ == "__main__":
    s1 = Singleton()
    s2 = Singleton()

    print(f"s1 is s2: {s1 is s2}")  # True



import threading

# ----------------------------
# Singleton2 - Eager Locking
# ----------------------------
class Singleton2:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:  # Always lock
            if cls._instance is None:
                print("Creating new instance (Singleton2 - eager lock)")
                cls._instance = super(Singleton2, cls).__new__(cls)
        return cls._instance


# ----------------------------
# Singleton3 - Lazy Locking (Double-Checked)
# ----------------------------
class Singleton3:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:  # First check
            with cls._lock:
                if cls._instance is None:  # Second check
                    print("Creating new instance (Singleton3 - lazy lock)")
                    cls._instance = super(Singleton3, cls).__new__(cls)
        return cls._instance


# ----------------------------
# Test Function (Used for Both)
# ----------------------------
def test_singleton(singleton_class):
    def task():
        instance = singleton_class()
        print(f"{singleton_class.__name__} instance id: {id(instance)}")

    threads = [threading.Thread(target=task) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()


# ----------------------------
# Main Execution
# ----------------------------
if __name__ == "__main__":
    print("=== Testing Singleton2 (Eager Locking) ===")
    test_singleton(Singleton2)

    print("\n=== Testing Singleton3 (Lazy Locking) ===")
    test_singleton(Singleton3)



