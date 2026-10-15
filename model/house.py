from .premises import Premises
from .flat import Flat

class House(Premises):
    def __init__(self, address):
        self.address = address
        self.flats = []

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, value):
        if not value.strip():
            raise ValueError("Адрес не может быть пустым")
        self._address = value.strip()

    def add_flat(self, number):
        if any(f.number == number for f in self.flats):
            raise ValueError(f"Квартира #{number} уже есть в доме")
        f = Flat(number)
        self.flats.append(f)
        return f

    def area(self):
        return sum(f.area() for f in self.flats)

    def volume(self):
        return sum(f.volume() for f in self.flats)

    def __len__(self):
        return len(self.flats)

    def __repr__(self):
        return f"House({self.address}, {len(self.flats)} flats)"
