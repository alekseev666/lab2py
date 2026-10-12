from .flat import Flat

class House:
    def __init__(self, address):
        self.address = address
        self.flats = []

    def add_flat(self, number):
        f = Flat(number)
        self.flats.append(f)
        return f

    def total_area(self):
        return sum(f.total_area() for f in self.flats)

    def total_volume(self):
        return sum(f.total_volume() for f in self.flats)

    #Формула Q = (V * (T_in-T_out) * K)/860
    def heat_power(self, t_in, t_out, k):
        return (self.total_volume() * (t_in - t_out) * k) / 860

    def __repr__(self):
        return f"House({self.address}, {len(self.flats)} flats)"