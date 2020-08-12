import abc
from Source.ChessUtils.Color import Color


class Player:
    __metaclass__ = abc.ABCMeta
    color: Color
    elo: int
    name: str

    def __init__(self, name: str):
        self.name = name
        self.elo = 1300
