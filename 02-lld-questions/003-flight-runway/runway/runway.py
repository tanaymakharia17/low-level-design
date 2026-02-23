import threading

class Runway:
    _id = None
    _lock = threading.Lock()

    def __init__(self, id):
        self._id = id
    
    def getLock(self):
        return self._lock
    
    def __str__(self):
        return f"runway({self._id})"