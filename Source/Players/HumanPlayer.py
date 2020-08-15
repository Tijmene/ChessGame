from Source.Board.GameBoard import GameBoard
from Source.ChessUtils.Move import Move
from Source.Players.Player import Player


class HumanPlayer(Player):
    """ This class could hold player specific information or characteristics """

    def get_next_move(self, board: GameBoard) -> Move:
        """ Gets input from the GUI """
        pass
