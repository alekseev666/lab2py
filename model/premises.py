from abc import ABC, abstractmethod

class Premises(ABC):

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def volume(self):
        pass

    #Формула Q = (V * (T_in-T_out) * K)/860
    def heat_power(self, t_in, t_out, k):
        if t_in <= t_out:
            raise ValueError("Температура в здании должна быть выше, чем на улице")
        if not 0.6 <= k <= 4:
            raise ValueError("Коэффициент рассеивания должен быть от 0.6 до 4")
        return (self.volume() * (t_in - t_out) * k) / 860

    @staticmethod
    def check_positive(value, name):
        if value <= 0:
            raise ValueError(f"{name} должна быть больше нуля")
        return value

    def __eq__(self, other):
        if not isinstance(other, Premises):
            return NotImplemented
        return self.area() == other.area()

    def __lt__(self, other):
        if not isinstance(other, Premises):
            return NotImplemented
        return self.area() < other.area()
