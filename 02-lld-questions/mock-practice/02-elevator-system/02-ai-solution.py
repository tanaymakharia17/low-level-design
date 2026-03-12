# Elevator System — AI Reference Solution
#
# ============================================================================
# INTERVIEW FLOW
# ============================================================================
#
# PHASE 1: Requirements Clarification (3-5 min)
# ----------------------------------------------
# Ask these out loud:
# 1. "What does a request look like? User on floor 5 presses UP — do they
#     also specify destination, or only after the elevator arrives?"
#     -> Two-step: external request (pickup), then internal request (destination)
# 2. "What scheduling algorithm? FCFS, nearest, SCAN/LOOK?"
#     -> Start simple (nearest idle), mention LOOK as extension
# 3. "Should elevators handle multiple passengers going to different floors?"
#     -> Yes, that's the point of SCAN — service floors in one direction
# 4. "How do we handle capacity? Reject at door or don't send full elevators?"
#     -> Don't dispatch to full elevators. If all full, queue the request.
#
#
# PHASE 2: Identify Entities + Pattern (3-5 min)
# -----------------------------------------------
# "This needs:
#   - Strategy pattern for scheduling (swappable algorithms)
#   - State/Enum for elevator direction + status
#   - Threading with Condition variables (elevators sleep until they have work)
#   - A controller to tie it together"
#
# Key model insight:
#   A Request has TWO phases:
#     1. External: "I'm on floor 5, going UP" → elevator comes to floor 5
#     2. Internal: "Take me to floor 9" → elevator adds floor 9 to its stops
#   The elevator's stop list contains BOTH pickup floors and destination floors.
#
#
# PHASE 3: Class Design (5 min)
# ------------------------------
# - Direction enum (UP, DOWN)
# - ElevatorState enum (IDLE, MOVING_UP, MOVING_DOWN, DOOR_OPEN)
# - Request (source_floor, destination_floor)
# - Elevator (id, current_floor, state, capacity, stops, condition_var)
#     - add_stop(floor), run()
# - SchedulingStrategy (ABC) -> NearestElevatorStrategy
# - ElevatorController (elevators, strategy, request handling)
#
#
# PHASE 4: Implementation (25-30 min)
# ------------------------------------


from __future__ import annotations
from abc import ABC, abstractmethod
from enum import Enum
import threading
import time


# ---- Enums ----

class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"


class ElevatorState(Enum):
    IDLE = "IDLE"
    MOVING_UP = "MOVING_UP"
    MOVING_DOWN = "MOVING_DOWN"


# ---- Models ----

class Request:
    """External request: user on source_floor wants to go to dest_floor."""

    _id_counter = 0

    def __init__(self, source_floor: int, dest_floor: int):
        Request._id_counter += 1
        self.id = Request._id_counter
        self.source_floor = source_floor
        self.dest_floor = dest_floor

    @property
    def direction(self) -> Direction:
        return Direction.UP if self.dest_floor > self.source_floor else Direction.DOWN

    def __repr__(self):
        return f"Req#{self.id}(floor {self.source_floor}→{self.dest_floor})"


# ---- Elevator ----

class Elevator:
    def __init__(self, elevator_id: int, capacity: int, total_floors: int):
        self.id = elevator_id
        self.current_floor = 0
        self.capacity = capacity
        self.total_floors = total_floors
        self.state = ElevatorState.IDLE
        self.passengers = 0

        # Stops this elevator needs to visit, with direction tracking
        self._up_stops: set[int] = set()
        self._down_stops: set[int] = set()

        # Condition variable — elevator sleeps until it has stops
        self._lock = threading.Lock()
        self._has_work = threading.Condition(self._lock)

        self._running = True

    def add_stop(self, floor: int, direction: Direction):
        """Add a floor stop. Thread-safe. Wakes the elevator if sleeping."""
        with self._has_work:
            if direction == Direction.UP:
                self._up_stops.add(floor)
            else:
                self._down_stops.add(floor)
            self._has_work.notify()

    def board_passenger(self) -> bool:
        """Returns True if a passenger can board (capacity check)."""
        with self._lock:
            if self.passengers >= self.capacity:
                return False
            self.passengers += 1
            return True

    def exit_passenger(self):
        with self._lock:
            self.passengers = max(0, self.passengers - 1)

    def has_stops(self) -> bool:
        return len(self._up_stops) > 0 or len(self._down_stops) > 0

    def stop(self):
        with self._has_work:
            self._running = False
            self._has_work.notify()

    def run(self):
        """Main elevator loop. Uses LOOK algorithm:
        Go up servicing all up-stops, then go down servicing all down-stops."""
        while self._running:
            with self._has_work:
                while not self.has_stops() and self._running:
                    self.state = ElevatorState.IDLE
                    self._has_work.wait()

                if not self._running:
                    break

                # Decide direction: prefer continuing current, else switch
                if self.state == ElevatorState.MOVING_UP and self._up_stops:
                    direction = Direction.UP
                elif self.state == ElevatorState.MOVING_DOWN and self._down_stops:
                    direction = Direction.DOWN
                elif self._up_stops:
                    direction = Direction.UP
                else:
                    direction = Direction.DOWN

            # Move in chosen direction (outside lock — movement takes time)
            if direction == Direction.UP:
                self._process_up()
            else:
                self._process_down()

    def _process_up(self):
        self.state = ElevatorState.MOVING_UP
        while True:
            with self._lock:
                if not self._up_stops:
                    break
                next_floor = min(self._up_stops)

            self._move_to(next_floor)

            with self._lock:
                self._up_stops.discard(next_floor)
            self._open_doors()

    def _process_down(self):
        self.state = ElevatorState.MOVING_DOWN
        while True:
            with self._lock:
                if not self._down_stops:
                    break
                next_floor = max(self._down_stops)

            self._move_to(next_floor)

            with self._lock:
                self._down_stops.discard(next_floor)
            self._open_doors()

    def _move_to(self, target: int):
        step = 1 if target > self.current_floor else -1
        while self.current_floor != target:
            time.sleep(0.3)  # simulate travel time per floor
            self.current_floor += step

    def _open_doors(self):
        print(f"  Elevator {self.id}: doors open at floor {self.current_floor} "
              f"[passengers: {self.passengers}]")
        time.sleep(0.2)  # simulate door open time

    def status(self) -> str:
        with self._lock:
            up = sorted(self._up_stops)
            down = sorted(self._down_stops, reverse=True)
        return (f"Elevator {self.id}: floor={self.current_floor}, "
                f"state={self.state.value}, passengers={self.passengers}, "
                f"up_stops={up}, down_stops={down}")


# ---- Scheduling Strategy ----

class SchedulingStrategy(ABC):
    @abstractmethod
    def select_elevator(self, request: Request, elevators: list[Elevator]) -> Elevator | None:
        pass


class NearestElevatorStrategy(SchedulingStrategy):
    """Pick the nearest elevator that is idle or moving toward the request floor
    in the same direction the user wants to go."""

    def select_elevator(self, request: Request, elevators: list[Elevator]) -> Elevator | None:
        best = None
        best_distance = float('inf')

        for elevator in elevators:
            if elevator.passengers >= elevator.capacity:
                continue

            distance = abs(elevator.current_floor - request.source_floor)

            # Prefer idle elevators or elevators heading toward this floor
            # in the right direction
            if elevator.state == ElevatorState.IDLE:
                score = distance
            elif (elevator.state == ElevatorState.MOVING_UP
                  and request.direction == Direction.UP
                  and elevator.current_floor <= request.source_floor):
                score = distance  # it'll pass by on the way up
            elif (elevator.state == ElevatorState.MOVING_DOWN
                  and request.direction == Direction.DOWN
                  and elevator.current_floor >= request.source_floor):
                score = distance  # it'll pass by on the way down
            else:
                score = distance + 100  # penalty: wrong direction or overshot

            if score < best_distance:
                best_distance = score
                best = elevator

        return best


# ---- Controller ----

class ElevatorController:
    def __init__(self, num_elevators: int, capacity: int,
                 total_floors: int, strategy: SchedulingStrategy):
        self.total_floors = total_floors
        self.strategy = strategy
        self.elevators: list[Elevator] = []
        self._threads: list[threading.Thread] = []

        for i in range(num_elevators):
            e = Elevator(i + 1, capacity, total_floors)
            self.elevators.append(e)
            t = threading.Thread(target=e.run, daemon=True)
            t.start()
            self._threads.append(t)

    def request_elevator(self, source_floor: int, dest_floor: int):
        """User on source_floor wants to go to dest_floor."""
        if not (0 <= source_floor <= self.total_floors):
            raise ValueError(f"Invalid source floor: {source_floor}")
        if not (0 <= dest_floor <= self.total_floors):
            raise ValueError(f"Invalid destination floor: {dest_floor}")
        if source_floor == dest_floor:
            raise ValueError("Source and destination cannot be the same")

        request = Request(source_floor, dest_floor)
        elevator = self.strategy.select_elevator(request, self.elevators)

        if elevator is None:
            print(f"  {request}: All elevators full, try again later")
            return

        direction = request.direction
        # Step 1: elevator goes to pickup floor
        elevator.add_stop(request.source_floor, direction)
        # Step 2: then goes to destination floor
        elevator.add_stop(request.dest_floor, direction)

        print(f"  {request} -> assigned to Elevator {elevator.id}")

    def display_status(self):
        print("  --- Elevator Status ---")
        for e in self.elevators:
            print(f"  {e.status()}")
        print("  -----------------------")

    def shutdown(self):
        for e in self.elevators:
            e.stop()
        for t in self._threads:
            t.join(timeout=2)


# ============================================================================
# PHASE 5: Demo (5 min)
# ============================================================================

def run():
    print("=" * 60)
    print("ELEVATOR SYSTEM DEMO")
    print("=" * 60)

    controller = ElevatorController(
        num_elevators=3,
        capacity=5,
        total_floors=15,
        strategy=NearestElevatorStrategy()
    )

    # --- Happy path: basic requests ---
    print("\n--- Requests: multiple users ---")
    controller.request_elevator(0, 5)   # lobby to 5
    controller.request_elevator(0, 10)  # lobby to 10
    controller.request_elevator(7, 2)   # floor 7 going down to 2

    time.sleep(3)
    controller.display_status()

    # --- More requests while elevators are moving ---
    print("\n--- Requests while elevators busy ---")
    controller.request_elevator(3, 8)   # floor 3 to 8
    controller.request_elevator(10, 1)  # floor 10 to 1

    time.sleep(4)
    controller.display_status()

    # --- Edge case: same floor ---
    print("\n--- Edge case: same floor ---")
    try:
        controller.request_elevator(5, 5)
    except ValueError as e:
        print(f"  Error (expected): {e}")

    # --- Edge case: invalid floor ---
    print("\n--- Edge case: invalid floor ---")
    try:
        controller.request_elevator(-1, 5)
    except ValueError as e:
        print(f"  Error (expected): {e}")

    try:
        controller.request_elevator(5, 20)
    except ValueError as e:
        print(f"  Error (expected): {e}")

    time.sleep(3)
    controller.display_status()

    controller.shutdown()
    print("\nDone.")


# ============================================================================
# PHASE 6: Discussion Points
# ============================================================================
#
# Q: "What scheduling algorithm is this?"
# A: LOOK algorithm — elevator goes up servicing all up-stops in order,
#    then reverses and services all down-stops. Unlike SCAN, it doesn't
#    go all the way to the top/bottom — it reverses at the last stop.
#
# Q: "How would you handle priority requests (e.g., fire mode)?"
# A: Add a priority field to Request. High-priority requests get added
#    to the front of the stop list. In fire mode, all elevators return
#    to ground floor and stop accepting requests.
#
# Q: "What about door hold / obstruction?"
# A: Add a DOOR_BLOCKED state. Elevator stays in DOOR_OPEN with a timeout.
#    If door sensor detects obstruction, reset the timeout. After max
#    retries, sound alarm and go out of service.
#
# Q: "How would you scale this to multiple buildings?"
# A: Each building has its own ElevatorController. A BuildingManager
#    routes requests to the right controller. No shared state between
#    buildings, so no cross-building locking needed.
#
# Q: "What if you needed to persist state across restarts?"
# A: Snapshot elevator positions and pending stops to a DB or file.
#    On restart, restore from snapshot. Pending requests that weren't
#    completed get re-queued.


# ============================================================================
# KEY DIFFERENCES FROM YOUR ATTEMPT
# ============================================================================
#
# 1.  threading.Condition instead of spin-loop
#     Your elevator.run() had `while True` with no sleep when idle.
#     This solution uses `self._has_work.wait()` — elevator sleeps
#     until add_stop() calls notify(). Zero CPU when idle.
#
# 2.  No deadlock
#     Your schedule_request held elevator.commands_list_lock then called
#     elevator.add_command which tried to acquire the same lock.
#     This solution: add_stop acquires _has_work (Condition wraps the lock),
#     and run() properly releases it during wait().
#
# 3.  LOOK algorithm with direction-aware stops
#     Your elevator had a flat command list with no direction awareness.
#     This solution has separate _up_stops and _down_stops sets.
#     Process all up stops (in ascending order), then all down stops
#     (in descending order). This is the standard elevator algorithm.
#
# 4.  Full request model: source + destination
#     Your Request had a floor and direction but no destination.
#     This solution: Request(source_floor=5, dest_floor=10).
#     Direction is derived. Both pickup and destination are added as stops.
#
# 5.  Direction-aware scheduling
#     Your strategy picked "first idle elevator" regardless of position.
#     This solution: prefers elevators that are idle OR already heading
#     toward the request floor in the right direction. Penalizes wrong-direction.
#
# 6.  Capacity is checked
#     Your max_capacity/current_capacity were never read.
#     This solution: scheduler skips full elevators, board_passenger()
#     returns False if at capacity.
#
# 7.  Display status
#     Missing from your attempt. This solution: display_status() shows
#     floor, state, passengers, pending stops for each elevator.
#
# 8.  Clean shutdown
#     Your elevator threads ran forever with no way to stop.
#     This solution: stop() sets _running=False and notifies the condition,
#     so run() exits cleanly. Daemon threads as safety net.
#
# 9.  Input validation
#     Your code accepted any floor number with no bounds check.
#     This solution: validates floor range and same-floor requests.
#
# 10. No stdout spam
#     Your "has no commands" printed millions of times in seconds.
#     This solution only prints meaningful events: door opens, status, assignments.


if __name__ == "__main__":
    run()
