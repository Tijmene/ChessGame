from enum import Enum


class Color(Enum):
    """
    All the colors of players in the game of chess.
    """
    BLACK = 0
    WHITE = 1

    def __str__(self):
        return self.name
