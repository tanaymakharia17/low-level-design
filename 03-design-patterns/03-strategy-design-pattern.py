from abc import ABC, abstractmethod

# -|> is a relationship
# -> has a relationship

# We have multiple Drive methods and to make it DRY we used strategy method

# Strategy Interface
class DriveStrategy(ABC):
    @abstractmethod
    def drive(self) -> None:
        pass
        
# Concrete Strategies
class SportyDriveStrategy(DriveStrategy):
    def drive(self) -> None:
        print("Sporty Drive")

class OffRoadStrategy(DriveStrategy):
    def drive(self) -> None:
        print("OffRoad Drive")

class NormalDriveStrategy(DriveStrategy):
    def drive(self) -> None:
        print("Normal Drive")

# Context
class Vehicle:
    def __init__(self, drive_strategy: DriveStrategy) -> None:
        self._drive_strategy = drive_strategy

    def drive(self) -> None:
        self._drive_strategy.drive()

    def set_drive_strategy(self, strategy: DriveStrategy) -> None:
        self._drive_strategy = strategy
    


# Concrete Vehicles
class SportyVehicle(Vehicle):
    def __init__(self) -> None:
        super().__init__(SportyDriveStrategy())

class OffRoadVehicle(Vehicle):
    def __init__(self) -> None:
        super().__init__(OffRoadStrategy())

class PassengerVehicle(Vehicle):
    def __init__(self) -> None:
        super().__init__(NormalDriveStrategy())



sporty = SportyVehicle()
sporty.drive()

offroad = OffRoadVehicle()
offroad.drive()

passanger = PassengerVehicle()
passanger.drive()