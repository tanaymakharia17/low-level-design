from .planes import Plane
from .enums import PlaneType

class MilitaryPlane(Plane):
    def __init__(self, id, name):
        self._plane_type = PlaneType.MILITARY
        self._id = id
        self._name = name
