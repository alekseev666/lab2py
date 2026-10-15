from .premises import Premises

class Room(Premises):
    def __init__(self, name, a, b, c):
        self.name = name
        self.a = a
        self.b = b
        self.c = c

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value.strip():
            raise ValueError("Название комнаты не может быть пустым")
        self._name = value.strip()

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        self._a = self.check_positive(value, "Длина")

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, value):
        self._b = self.check_positive(value, "Ширина")

    @property
    def c(self):
        return self._c

    @c.setter
    def c(self, value):
        self._c = self.check_positive(value, "Высота")

    def area(self):
        return self.a * self.b

    def volume(self):
        return self.area() * self.c

    def __repr__(self):
        return f"Room({self.name}, {self.a} x {self.b} x {self.c})"

    def __str__(self):
        return f"комната {self.name} ({self.area():.1f} м²)"
