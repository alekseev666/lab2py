class Room:
    def __init__(self, name, a, b, c ):
        self.name = name
        self.a = a
        self.b = b
        self.c = c

    def area(self):
        return self.a * self.b

    def volume(self):
        return self.area() * self.c
