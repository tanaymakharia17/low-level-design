from abc import ABC, abstractmethod
from enum import Enum
# Factory Pattern ->
# single source of truth in the entire application to get this shape object to make data consistent. Also very minimal changes'
# if we want to change the logic og shape

class Shape(ABC):
    
    @abstractmethod
    def draw(self):
        pass


class Circle(Shape):
    def draw(self):
        print("Circle")


class Square(Shape):
    def draw(self):
        print("Square")

class ShapeEnum(Enum):
    CIRCLE = 'circle'
    SQUARE = 'square'

class ShapeFactory:

    def getShape(self, shapeType: ShapeEnum):
        match shapeType:
            case ShapeEnum.CIRCLE:
                return Circle()
            case ShapeEnum.SQUARE:
                return Square()
            


shape_factory = ShapeFactory()
c = shape_factory.getShape(ShapeEnum.CIRCLE)
s = shape_factory.getShape(ShapeEnum.SQUARE)
c.draw()
s.draw()


# Abstract Factory -> (factory of factories)

class PremiumVehicleEnum(Enum):
    MERCEDES = 'mercedes'
    AUDI = 'audi'
    FERRARI = 'ferrari'


class Vehicle(ABC):
    @abstractmethod
    def getName(self):
        pass

class Mercedes(Vehicle):
    def getName(self):
        return PremiumVehicleEnum.MERCEDES.name

class Audi(Vehicle):
    def getName(self):
        return PremiumVehicleEnum.AUDI.name

class Ferrari(Vehicle):
    def getName(self):
        return PremiumVehicleEnum.FERRARI.name

class VehicleFactory(ABC):

    @abstractmethod
    def getVehicle(self):
        pass




class PremiumVehicleFactory(VehicleFactory):

    def getVehicle(self, vehicle_type: PremiumVehicleEnum):
        match vehicle_type:
            case PremiumVehicleEnum.MERCEDES:
                return Mercedes()
            case PremiumVehicleEnum.AUDI:
                return Audi()
            case PremiumVehicleEnum.FERRARI:
                return Ferrari()


class VechileFactoryEnum(Enum):
    PREMIUM = 'premium'
    REGULAR = 'regular'

class VehicleFactoryFactory:
    def getFactory(self, factory_type: VechileFactoryEnum):
        match factory_type:
            case VechileFactoryEnum.PREMIUM:
                return PremiumVehicleFactory()
            # case VechileFactoryEnum.REGULAR:
            #     return


vehicle_factory_factory = VehicleFactoryFactory()

premium_factory = vehicle_factory_factory.getFactory(VechileFactoryEnum.PREMIUM)

audi_vehicle = premium_factory.getVehicle(PremiumVehicleEnum.AUDI)
ferrari_vehicle = premium_factory.getVehicle(PremiumVehicleEnum.FERRARI)
print(audi_vehicle.getName())
print(ferrari_vehicle.getName())