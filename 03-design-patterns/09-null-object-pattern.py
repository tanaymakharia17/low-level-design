

# class Vehicle:
#     def getName(self):
#         print("BMW")


# def printVehicleDetail(vehicle1: Vehicle):
#     vehicle1.getName()


# This will throw error if vehicle is a null value

from abc import ABC, abstractmethod

class Vehicle(ABC):

    @abstractmethod
    def getName(self):
        pass


class EngineVehicle(Vehicle):
    def getName(self):
        print("This vehicle has an engine.")


class NullVehicle(Vehicle):
    def getName(self):
        print("This is an null class")

class VehicleFactory:
    def getVehicle(self, type):
        match type:
            case "car":
                return EngineVehicle()
        return NullVehicle()

def printVehicleDetail(vehicle1: Vehicle):
    vehicle1.getName()

factory = VehicleFactory()
vehicle = factory.getVehicle("Cycle")
print(vehicle)
printVehicleDetail(vehicle)