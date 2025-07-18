

"""

Requirements:
Multiple elevators
Multiple elevator assigning stratigies
Multiple state of an elevator
Command of floor and and arrow


classes:
Abstract elevator+ multiple types of elevator (capacity+other details)
Mutiple strategy of elecator assigining abstract class
Nearestfirststrategy
State abstract class
multiple state class - idle + moving
Elevator controller class



Command request class with floor and dxn


"""
from __future__ import annotations
import threading

from abc import ABC, abstractmethod
import time
import random





class AbstractElevatorState(ABC):
    
    @abstractmethod
    def move(self, elevator: AbstractElevator, floor): pass




class IdleState(AbstractElevatorState):
    def move(self, elevator: AbstractElevator, floor):
        elevator.setState(elevator.moving_state)
        elevator.destination_floor = floor
        start_floor = elevator.current_floor
        end_floor = elevator.destination_floor
        floors = []
        if start_floor <= end_floor:
            floors = list(range(start_floor+1, end_floor + 1))
        else:
            floors = list(range(start_floor-1, end_floor - 1, -1))
        
        for current_floor in floors:
            time.sleep(0.8)
            elevator.current_floor = current_floor
            print(f"{elevator} is on floor {current_floor}.")
        elevator.destination_floor = None
        elevator.setState(elevator.idle_state)



class MovingState(AbstractElevatorState):
    
    def move(self, elevator: AbstractElevator, floor):
        print(f"Elevator: {elevator} is on floor {self.current_floor} and is moving to floor {self.destination_floor}")




class AbstractElevator(ABC):
    capacity: int
    id: int

    def __init__(self, id, capacity):
        self.id = id
        self.capacity = capacity
        self.current_floor = 0
        self.destination_floor = None
        self.idle_state = IdleState()
        self.moving_state = MovingState()
        self.state = self.idle_state
        self.current_capacity = 0
    
    def __repr__(self):
        return f"E({self.id})"


    def move(self, destination_floor): self.state.move(self, destination_floor)
    def setState(self, state:AbstractElevatorState): self.state = state


class ACElevator(AbstractElevator):
    pass


class FanElevator(AbstractElevator):
    pass


class Command:
    def __init__(self, floor):
        self.floor = floor

class ElevatorAssiginingStrategy(ABC):
    
    @abstractmethod
    def getElevator(self, command: Command, elevators: list[AbstractElevator]) -> AbstractElevator: pass


class NearestIdleElevatorStrategy(ElevatorAssiginingStrategy):

    def getElevator(self, command, elevators) -> AbstractElevator:
        elevators = random.sample(elevators, k=len(elevators))
        destination_floor = command.floor
        optimal_elevator, distance = None, 1000000
        for elevator in elevators:
            if isinstance(elevator.state, IdleState):
                elevator_distance = abs(elevator.current_floor - destination_floor)
                if elevator_distance < distance:
                    optimal_elevator = elevator
                    distance = elevator_distance
        
        return optimal_elevator



class ElevatorController:
    

    def __init__(self, elevators: list[AbstractElevator], elevator_assigining_strategy: ElevatorAssiginingStrategy):
        self.elevators = elevators
        self.elevator_assigining_strategy = elevator_assigining_strategy
    

    def processCommand(self, command: Command):
        destination_floor = command.floor
        optimal_elevator = None
        while optimal_elevator == None:
            optimal_elevator = self.elevator_assigining_strategy.getElevator(command, self.elevators)
        
        print(f"Assigned elevator: {optimal_elevator}")
        optimal_elevator.move(destination_floor)





# def simulate_user_commands(controller, commands, delay_between=1.5):
#     for i, command in enumerate(commands):
#         print(f"\n🛎️  [Request {i+1}] Requesting floor: {command.floor}")
#         threading.Thread(target=controller.processCommand, args=(command,)).start()
#         time.sleep(delay_between)  # simulate time between different requests


# if __name__ == "__main__":
#     # Create elevators
#     elevators = [
#         ACElevator(1, 10),
#         FanElevator(2, 12),
#         FanElevator(3, 11)
#     ]

#     # Elevator assigning strategy
#     eas = NearestIdleElevatorStrategy()

#     # Elevator controller
#     ec = ElevatorController(elevators, eas)

#     # User floor commands
#     commands = [
#         Command(3),
#         Command(7),
#         Command(4),
#         Command(11),
#         Command(15),
#         Command(11),
#         Command(10),
#         Command(7)
#     ]

#     # Simulate command requests from users
#     simulate_user_commands(ec, commands)



if __name__ == "__main__":
    elevators = [
        ACElevator(1, 10),
        FanElevator(2, 12),
        FanElevator(3, 11)
    ]
    strategy = NearestIdleElevatorStrategy()
    controller = ElevatorController(elevators, strategy)

    commands = [
        Command(3),
        Command(7),
        Command(4),
        Command(11),
        Command(15),
        Command(11),
        Command(10),
        Command(7)
    ]

    for i, command in enumerate(commands, 1):
        print(f"\n🛎️  [Request {i}] Requesting floor: {command.floor}")
        controller.processCommand(command)