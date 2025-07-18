from runway.runway import Runway
from planes.planes import Plane
from request.request import Request
from request.enums import PriorityType
import time
import threading

class PlaneRunwayController:
    _instance = None
    _runways = []
    _planes = []
    _request = []

    def __init__(self):
        self._lock = threading.Lock()
        self._condition = threading.Condition(self._lock)


    def addRunway(self, runway: Runway):
        self._runways.append(runway)
            

    def addPlane(self, plane: Plane):
        self._planes.append(plane)
    
    def addRequest(self, request: Request):
        with self._condition:
            if PriorityType.LOW:
                self._request.append(request)
            elif PriorityType.HIGH:
                self._request.appendLeft(request)
            print("---------------------------------------------------")
            print(f"Added: {request.plane}({request.priority})")
            print("---------------------------------------------------")
            self._condition.notify()
    
    def processRequest(self):
        while True:
            with self._condition:
                while not self._request:
                    self._condition.wait()

                assigned_runway = None

                while assigned_runway is None:
                    for runway in self._runways:
                        if runway.getLock().acquire(blocking=False):
                            assigned_runway = runway
                            break
                
                request = self._request.pop(0)
                threading.Thread(target=self._handle_runway, args=(request, assigned_runway)).start()
                
    
    def _handle_runway(self, request: Request, runway: Runway):
        print(f"Plane {request.plane} is running on runway {runway}. Priority: {request.priority.name}")
        time.sleep(5)
        print(f"Runway {runway} is free")
        runway.getLock().release()



