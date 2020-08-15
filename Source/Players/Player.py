import abc
from Source.ChessUtils.Color import Color
from Source.Board.GameBoard import GameBoard
from Source.ChessUtils.Move import Move


class Player:
    """ A player has to implement the get_next_move method """

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

    @abc.abstractmethod
    def get_next_move(self, board: GameBoard) -> Move:
        return

    def __str__(self):
        return "Player named {name} with elo: {elo}. " \
               "Currently plays {color} and has {points} points.".format(name=self.name,
                                                                         elo=self.elo,
                                                                         color=self.color,
                                                                         points=self.points_earned)

