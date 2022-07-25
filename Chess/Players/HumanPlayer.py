from Chess.Board.GameBoard import GameBoard
from Chess.ChessUtils.Color import Color
from Chess.ChessUtils.Move import Move
from Chess.Players.Player import Player
import queue


class HumanPlayer(Player):
    """
    This class holds player specific information or characteristics
    """
    gui_connection: queue.Queue

    def __init__(self, name: str, color: Color):
        super().__init__(name, color)
        self.gui_connection = queue.Queue()  # Human players need a connection to the GUI

    def get_next_move(self, board: GameBoard) -> Move:
        """
        Human players get their moves by interacting with the gui and do not directly use the board variable.
        :param board: :class:`GameBoard` describes the current state of the game board.
        :return: the :class:`Move` decided on by the player via the GUI
        """
        response = self.gui_connection.get()
        assert isinstance(response, Move), f"Expected a response of type Move but received response: {response} " \
                                           f"with type {type(response)}"
        return response
