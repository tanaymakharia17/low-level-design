from .enums import PlaneType
from .cargoPlane import CargoPlane
from .militaryPlane import MilitaryPlane
from .privatePlane import PrivatePlane

class PlaneFactory:

    def getPlane(self, plane_type: PlaneType, _id, name):
        if plane_type == PlaneType.CARGO:
            return CargoPlane(_id, name)
        elif plane_type == PlaneType.MILITARY:
            return MilitaryPlane(_id, name)
        elif plane_type == PlaneType.PRIVATE:
            return PrivatePlane(_id, name)