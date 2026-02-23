from abc import ABC, abstractmethod


class Plane(ABC):
    _id = None
    _name = ""

    def __str__(self):
        return f"{self._name}({self._id})"

