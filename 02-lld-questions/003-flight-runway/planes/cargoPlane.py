from .planes import Plane
from .enums import PlaneType

class CargoPlane(Plane):
    def __init__(self, id, name):
        self._plane_type = PlaneType.CARGO
        self._id = id
        self._name = name
