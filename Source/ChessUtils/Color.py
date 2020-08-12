from enum import Enum


class Color(Enum):
    BLACK = 0
    WHITE = 1

    def __str__(self):
        return self.name
