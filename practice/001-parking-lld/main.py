
"""

Flow:
1. Car comes to the gate
2. Car owner takes a ticket and parks the car to position mentioned in the ticket
3. After the Car owner exists he pays the bill and leaves

Requirements:
1. Vehicle can be of multiple types: two wheeler, 4 wheeler, truck, etc.
2. Park the car nearest to elevator, exit, etc.
3. When car exists calculate and take payment.

possible classes:
VehicleEnum (multiple types)
gate (multiple gates and can be used as both entry and exit)
Ticket (which the user takes)
Parking spot (multiple types)
"""

from abc import ABC, abstractmethod

class ParkingSpot:
    def __init__(self, parking_spot_type, price, location):
        self.parking_spot_type = parking_spot_type
        self.price = price
        self.isEmpty = True
        self.location = location

    def parkVehicle(self):
        self.isEmpty = False

    def freeSpot(self):
        self.isEmpty = True


class Gate:
    def createTicket(self, vehicle_type):
        pass
    
    def collectPayment(self, ticket):
        pass

class Ticket:
    def __init__(self, timestamp, vehicle_type, parking_spot):
        self.timestamp = timestamp
        self.vehicle_type = vehicle_type
        self.parking_spot = parking_spot




class ParkingLotController:
    parking_spots: list[ParkingSpot] = []

    def createParkingSpot()





