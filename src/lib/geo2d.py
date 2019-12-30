EPSILON = 1e-9

def almost_equal(a, b):
    return abs(a-b) < EPSILON

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y+other.y)

    def __abs__(self):
        return Point(abs(self.x), abs(self.y))

    def __eq__(self, other):
        return other and almost_equal(self.x, other.x) and almost_equal(self.y, other.y)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __lt__(self, other):
        if almost_equal(self.y, other.y):
            if almost_equal(self.x, other.x):
                return 0
            return self.x < other.x
        return self.y < other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return '({0}, {1})'.format(self.x, self.y)


NORTH = Point(0, -1)
NORTH_EAST = Point(1, -1)
EAST = Point(1, 0)
SOUTH_EAST = Point(1,1)
SOUTH = Point(0, 1)
SOUTH_WEST = Point(-1,1)
WEST = Point(-1, 0)
NORTH_WEST = Point(-1, -1)

DIRECTIONS = [NORTH, EAST, SOUTH, WEST]
DIRECTIONS_INCL_DIAGONALS = [NORTH, NORTH_EAST, EAST, SOUTH_EAST, SOUTH, SOUTH_WEST, WEST, NORTH_WEST]
