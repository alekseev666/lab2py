from .premises import Premises
from .room import Room

class Flat(Premises):
    CEILING = 2.5  # высота потолка в панельном доме, м

    def __init__(self, number):
        self.number = number
        self.rooms = []

    @property
    def number(self):
        return self._number

    @number.setter
    def number(self, value):
        if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
            raise ValueError("Номер квартиры должен быть целым числом больше нуля")
        self._number = value

    def add_room(self, name, a, b):
        r = Room(name, a, b, self.CEILING)
        self.rooms.append(r)
        return r

    def area(self):
        return sum(r.area() for r in self.rooms)

    def volume(self):
        return sum(r.volume() for r in self.rooms)

    def __len__(self):
        return len(self.rooms)

    def __repr__(self):
        return f"квартира #{self.number} ({len(self.rooms)} комнат)"
