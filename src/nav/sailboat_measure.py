import math

MAX_TACK_ANGLE = math.pi / 4


class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, coord):
        y = coord.y - self.y
        x = coord.x - self.x

        if y > 0 and abs(math.atan(y / x)) < MAX_TACK_ANGLE:
            return y / math.cos(MAX_TACK_ANGLE)

        return math.sqrt(x ** 2 + y ** 2)
