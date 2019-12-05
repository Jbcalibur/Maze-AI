from enum import Enum

class Cell(Enum):
    FLOOR = ' '
    WALL = '#'
    START = 'S'
    FINISH = 'F'


class Direction(Enum):
    LEFT = 'l'
    UP = "u"
    RIGHT = 'r'
    DOWN = "d"