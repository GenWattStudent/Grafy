import math
import random


class Vector:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

    def __rmul__(self, scalar: float) -> "Vector":
        return self * scalar

    def __truediv__(self, other):
        return Vector(self.x / other, self.y / other)

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y))

    def __abs__(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def random(self, min_x: float, max_x: float, min_y: float, max_y: float):
        self.x = random.uniform(min_x, max_x)
        self.y = random.uniform(min_y, max_y)
        return self

    def length(self):
        return abs(self)

    def distance(self, other):
        return (self - other).length()

    def normalized(self) -> "Vector":
        length = abs(self)
        if length > 0:
            return self / length
        else:
            return Vector(0, 0)
    
    def angle_to(self, other_vector):
        dx = other_vector.x - self.x
        dy = other_vector.y - self.y
        return math.atan2(dy, dx)
