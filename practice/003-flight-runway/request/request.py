from .enums import PriorityType
from planes.planes import Plane

class Request:
    plane: Plane = None
    priority: PriorityType = None

    def __init__(self, plane: Plane, priority: PriorityType):
        self.plane = plane
        self.priority = priority
    