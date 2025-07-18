
from .planes import Plane
from .enums import PlaneType

class PrivatePlane(Plane):
    def __init__(self, id, name):
        self._plane_type = PlaneType.PRIVATE
        self._id = id
        self._name = name
