import abc
import queue

from Chess.ChessUtils.Color import Color
from Chess.Board.GameBoard import GameBoard
from Chess.ChessUtils.Move import Move


class Player:
    """ A player has to implement the get_next_move method """

    __metaclass__ = abc.ABCMeta
    name: str
    color: Color
    elo: int
    points_earned: int
    running: bool
    move_out_box: queue.Queue
    inbox: queue.Queue

    def __init__(self, name: str, color: Color):
        self.name = name
        self.color = color
        self.elo = 1300
        self.points_earned = 0
        self.inbox = queue.Queue()

    def run(self) -> None:
        self.running = True
        while self.running:
            board = self.inbox.get()
            move = self.get_next_move(board)
            self.move_out_box.put(move)

    def kill(self) -> None:
        self.running = False

    def plays_white(self):
        return Color.WHITE == self.color

    def plays_black(self):
        return Color.BLACK == self.color

    def connect_to_game(self, move_in_box: queue.Queue) -> None:
        self.move_out_box = move_in_box

    @abc.abstractmethod
    def get_next_move(self, board: GameBoard) -> Move:
        pass

    def __str__(self):
        return f"Player named {self.name} with elo: {self.elo}. " \
               f"Currently plays {self.color} and has {self.points_earned} points."

