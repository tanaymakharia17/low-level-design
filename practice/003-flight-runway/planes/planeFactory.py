from .enums import PlaneType
from .cargoPlane import CargoPlane
from .militaryPlane import MilitaryPlane
from .privatePlane import PrivatePlane

class PlaneFactory:

    def getPlane(self, plane_type: PlaneType, _id, name):
        match plane_type:
            case PlaneType.CARGO:
                return CargoPlane(_id, name)
            case PlaneType.MILITARY:
                return MilitaryPlane(_id, name)
            case PlaneType.PRIVATE:
                return PrivatePlane(_id, name)