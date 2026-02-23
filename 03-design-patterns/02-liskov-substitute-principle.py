from abc import ABC, abstractmethod

# Before hasEngine was in Vehicle and when we inherit Vehicle in 
# Bicycle then it will give run time error of calling hasEngine on it now(after creating EngineVehicle) 
# we are getting compile time error

class Vehicle:

    def getNumberOfWheels(self) -> int:
        return 2
    
    

class EngineVehicle(Vehicle):
    def hasEngine(self) -> bool:
        return True
    

class MotorCycle(EngineVehicle):
    pass

class Car(EngineVehicle):

    def getNumberOfWheels(self) -> int:
        return 4

class Bicycle(Vehicle):
    pass


vehicles = []
vehicles.append(MotorCycle())
vehicles.append(Car())
vehicles.append(Bicycle())

for vehicle in vehicles:
    try:
        print(vehicle.hasEngine()) # Now we have compile time error
    except:
        print("Error")
        print("-----------------")
        print(isinstance(vehicle, Bicycle))
        print("-----------------")

