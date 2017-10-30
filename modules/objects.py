"""Модуль реализует основные объекты игры «Pacman»"""

from enum import Enum


class Cell:
    """Класс клетки поля"""

    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def cycling(self, size):
        width, height = size
        self.X = (self.X + width) % width
        self.Y = (self.Y + height) % height
        return self

    def __eq__(self, value):
        if not isinstance(value, Cell):
            raise TypeError("Type of value is not Cell")
        return self.X == value.X and self.Y == value.Y

    def __add__(self, value):
        if isinstance(value, Cell):
            return Cell(self.X + value.X, self.Y + value.Y)
        if isinstance(value, Direction):
            return Cell(self.X + value.value.X, self.Y + value.value.Y)
        raise TypeError("Type of value is not Cell")

    def __radd__(self, value):
        return self.__add__(value)

    def __mul__(self, other):
        if not isinstance(other, int):
            raise TypeError("Type of value is not int")
        return Cell(self.X * other, self.Y * other)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __sub__(self, value):
        if isinstance(value, Cell):
            return Cell(self.X - value.X, self.Y - value.Y)
        if isinstance(value, Direction):
            return Cell(self.X - value.value.X, self.Y - value.value.Y)
        raise TypeError("Type of value is not Cell")

    def __str__(self):
        return "Cell({}, {})".format(self.X, self.Y)

    def __neg__(self):
        return Cell(-self.X, - self.Y)

    # def __index__(self):
    #     return (self.X, self.Y)


class CellState(Enum):
    """Класс состояния клекти"""

    EMPTY = 0
    WALL = 1
    POINT = 2
    CHERRY = 3
    ENERGIZER = 4


class Map:
    """Класс карты уровня"""

    def __init__(self):
        self.width = 0
        self.height = 0
        self.objects = []

    def __getitem__(self, point):
        x, y = point
        return self.objects[x][y]

    def __setitem__(self, point, value):
        x, y = point
        self.objects[x][y] = value

    def getwidth(self):
        return 0 if self.height == 1 else len(self.objects[0])

    def getheight(self):
        return len(self.objects)

    def __len__(self):
        return len(self.objects)

    def objectsCount(self):
        return len(self)


class Direction(Enum):
    """Класс всевозможных направлений персонажей игры"""

    LEFT = Cell(-1, 0)
    UP = Cell(0, -1)
    DOWN = Cell(0, 1)
    RIGHT = Cell(1, 0)


class Entity:
    """Класс персонажа игры"""

    def __init__(self, loc, dir):
        self.location = loc
        self.direction = dir


class Ghost(Entity):

    def __init__(self, loc, dir):
        super().__init__(loc, dir)
        self.state = GhostState.CHASE


class GhostState(Enum):

    CHASE = 0
    SCATTER = 1
    FRIGHTENED = 2


class Queue(list):

    def __init__(self, *args):
        super().__init__()
        self.extend(list(args))

    def empty(self):
        return not bool(self)

    def enqueue(self, value):
        self.append(value)
        return self

    def dequeue(self):
        return self.pop(0)

    def peek(self):
        return self[0]
