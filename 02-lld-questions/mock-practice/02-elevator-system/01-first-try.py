# Elevator System — First Attempt
# Time limit: 45 minutes
#
# Requirements:
# - Building with N floors and M elevators
# - Users can request an elevator from any floor (up/down)
# - Users inside can select destination floor
# - Elevator scheduling algorithm (e.g., SCAN/LOOK)
# - Elevators have capacity limits
# - Display current status of all elevators
#
# START CODING BELOW:



# Request:
#     - id
#     - floor
#     - direction


# ElevatorState:
#     - IDLE
#     - MOVING
#     - DOOR_OPEN

# Elevator:
#     - id
#     - state
#     - commands: list[Command]
#     - current_floor
#     - destination_floor
#     - max_capacity
#     - current_capacity

#     - run(): # a constant running process


# RequestQueue:
#     - requests: list[Request]\
#     - lock: Lock
#     - add_request(request: Request)
#     - get_next_request()
#     - is_empty()


# RequestScheduler(Abstract):
#     - start(request_queue: RequestQueue, elevators: list[Elevator]):


# NearestIdleElevatorStrategy(RequestScheduler):
#     - start(request: Request, elevators: list[Elevator]) -> Elevator

# ElevatorController:
#     - scheduler: RequestScheduler
#     - elevators: list[Elevator]
#     - start_scheduler()
#     - add_request(request: Request)
#     - add_elevator(elevator: Elevator)





from __future__ import annotations
from abc import ABC, abstractmethod
import threading
from enum import Enum
import time

class Request:
    def __init__(self, id: int, floor: int, direction: Direction):
        self.id = id
        self.floor = floor
        self.direction = direction

class Direction(Enum):
    UP = "up"
    DOWN = "down"

class ElevatorState(Enum):
    IDLE = "idle"
    MOVING = "moving"
    DOOR_OPEN = "door_open"

class Command:
    def __init__(self, id: int, floor: int):
        self.id = id
        self.floor = floor

class Elevator:
    def __init__(self, id: int, max_capacity: int):
        self.id = id
        self.state = ElevatorState.IDLE
        self.current_floor = 0
        self.max_capacity = max_capacity
        self.current_capacity = 0
        self.commands = []
        self.commands_list_lock = threading.Lock()
    
    def run(self):
        while True:
            command = None
            with self.commands_list_lock:
                if len(self.commands) == 0:
                    print(f"Elevator {self.id} has no commands")
                    continue
                print(f"Elevator {self.id} has commands: {self.commands}")
                command = self.commands[0]
                self.commands.pop(0)

            self.destination_floor = command.floor
            self.state = ElevatorState.MOVING
            self.move()
            self.state = ElevatorState.DOOR_OPEN
            print(f"Elevator {self.id} is on floor {self.current_floor}")
            time.sleep(1)
            self.state = ElevatorState.IDLE


    def add_command(self, command: Command, pos: int = -1):
        with self.commands_list_lock:
            if pos == -1:
                self.commands.append(command)
            else:
                self.commands.insert(pos, command)
        
    def move(self):
        if self.current_floor == None or self.destination_floor == None:
            return
        if self.current_floor == self.destination_floor:
            return
        floors = []
        if self.current_floor < self.destination_floor:
            floors = list(range(self.current_floor + 1, self.destination_floor + 1))
        else:
            floors = list(range(self.current_floor - 1, self.destination_floor - 1, -1))
        for floor in floors:
            self.current_floor = floor
            time.sleep(0.8)
            print(f"Elevator {self.id} is on floor {self.current_floor}")
        

        self.destination_floor = None
    


class RequestScheduler(ABC):
    @abstractmethod
    def schedule_request(self, request: Request, elevators: list[Elevator]) -> Elevator:
        pass

    @abstractmethod
    def start(self, request_queue: RequestQueue, elevators: list[Elevator]):
        pass

class NearestIdleElevatorStrategy(RequestScheduler):
    def schedule_request(self, request: Request, elevators: list[Elevator]) -> Elevator:
        while True:
            for elevator in elevators:
                with elevator.commands_list_lock:
                    if len(elevator.commands) == 0:
                        print(f"Elevator {elevator.id} is idle, adding command: {request.id} to floor {request.floor}")
                        elevator.add_command(Command(request.id, request.floor))
                        print(f"Added command: {command.id} to floor {command.floor} to elevator {elevator.id}")
                        return
                    print(f"Elevator {elevator.id} has commands: {elevator.commands}")
    
    def start(self, request_queue: RequestQueue, elevators: list[Elevator]):
        while True:
            request = request_queue.get_next_request()
            if request is None:
                time.sleep(1)
                continue
            print(f"Scheduling request: {request.id} to floor {request.floor} in direction {request.direction}")
            self.schedule_request(request, elevators)

class RequestQueue:
    def __init__(self):
        self.requests = []
        self.lock = threading.Lock()
    
    def add_request(self, request: Request):
        with self.lock:
            print(f"Adding request: {request.id} to floor {request.floor} in direction {request.direction}")
            self.requests.append(request)
    
    def get_next_request(self) -> Request:
        with self.lock:
            if len(self.requests) == 0:
                return None
            print(f"Getting next request: {self.requests[0].id} from floor {self.requests[0].floor} in direction {self.requests[0].direction}")
            return self.requests.pop(0)

class ElevatorController:
    def __init__(self, request_scheduler: RequestScheduler):
        self.elevators = []
        self.request_scheduler = request_scheduler
        self.request_queue = RequestQueue()
    
    def start_scheduler(self):
        threading.Thread(target=self.request_scheduler.start, args=(self.request_queue, self.elevators)).start()
    
    def add_request(self, request: Request):
        self.request_queue.add_request(request)
    

    def add_elevator(self, elevator: Elevator):
        self.elevators.append(elevator)
        threading.Thread(target=elevator.run).start()



if __name__ == "__main__":
    elevator_controller = ElevatorController(NearestIdleElevatorStrategy())
    elevator_controller.start_scheduler()
    elevator_controller.add_elevator(Elevator(1, 10))
    elevator_controller.add_elevator(Elevator(2, 10))
    elevator_controller.add_request(Request(1, 5, Direction.UP))
    elevator_controller.add_request(Request(2, 3, Direction.DOWN))
    elevator_controller.add_request(Request(3, 7, Direction.UP))
    elevator_controller.add_request(Request(4, 2, Direction.DOWN))
    elevator_controller.add_request(Request(5, 8, Direction.UP))
    elevator_controller.add_request(Request(6, 1, Direction.DOWN))
    elevator_controller.add_request(Request(7, 6, Direction.UP))
    elevator_controller.add_request(Request(8, 4, Direction.DOWN))
    time.sleep(30)