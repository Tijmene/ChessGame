import abc
from Source.ChessUtils.Color import Color


class Player:

    __metaclass__ = abc.ABCMeta
    name: str
    color: Color
    elo: int
    points_earned: int = 0

    def __init__(self, name: str, color: Color):
        self.name = name
        self.color = color
        self.elo = 1300

    def plays_white(self):
        return Color.WHITE == self.color

    def plays_black(self):
        return Color.BLACK == self.color

