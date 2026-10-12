from .room import Room

class Flat:
    def __init__(self, number):
        self.number = number
        self.rooms = []

    def add_room(self, name, a, b, c):
        r = Room(name, a, b, c)
        self.rooms.append(r)
        return r

    def total_area(self):
        return sum(r.area() for r in self.rooms)

    def total_volume(self):
        return sum(r.volume() for r in self.rooms)

    def __repr__(self):
        return f"квартира #{self.number} ({len(self.rooms)} комнат)"