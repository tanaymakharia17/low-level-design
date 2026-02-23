"""
Multiple planes
Multiple runways

new runway added or freed then it is up for grabs
each plane have a priority

give higher priority plane more precendance

classes:
Planes interface
multiple plane classes
planes enums
planes factory

runway abstract
runways multiple types maybe?
runway factory

planerunwaycontroller
"""

from planeRunwayController import PlaneRunwayController
import threading
from planes.enums import PlaneType
from planes.planeFactory import PlaneFactory
from runway.runway import Runway
import time
from request.enums import PriorityType
from request.request import Request

airport = PlaneRunwayController()
plane_factory = PlaneFactory()
cargo_plane = plane_factory.getPlane(PlaneType.CARGO, 1, "Fedex")
# passanger_plane = plane_factory.getPlane(PlaneType.PASSANGER, 2, "Air India")
military_plane = plane_factory.getPlane(PlaneType.MILITARY, 3, "Indian Airforce")
private_plane = plane_factory.getPlane(PlaneType.PRIVATE, 4, "Ambani")
planes = [cargo_plane, military_plane, private_plane]
runways = []
for plane in planes:
    airport.addPlane(plane)

for i in range(2):
    runway = Runway(i)
    airport.addRunway(runway)
    runways.append(runway)


threading.Thread(target=airport.processRequest, daemon=True).start()

import random

def simulate_requests():
    for i in range (10):
        for plane in planes:
            # priority = random.choice(list(PriorityType))
            priority = PriorityType.HIGH if i == 7 or i==2 or i ==4  and plane == cargo_plane else PriorityType.LOW
            request = Request(plane, priority)
            airport.addRequest(request)
            time.sleep(0.5)

request_thread = threading.Thread(target=simulate_requests)
request_thread.start()

request_thread.join()



time.sleep(40)