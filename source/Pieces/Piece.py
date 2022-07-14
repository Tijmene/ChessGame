from source.Board import GameBoard
from source.ChessUtils.Position import Position
from source.ChessUtils.Color import Color
from source.ChessUtils.PossibleMoveSet import PossibleMoveSet
import abc


class Piece:
    """
    The abstract piece class, all functionality that is shared between all pieces is written into this class
    Some methods are labeled with the abstract annotation which means that they have to be implemented by any
    class that inherits from this class
    """
    __metaclass__ = abc.ABCMeta     # This declares this class as abstract.
    color: Color                    # An enum class is used to restrict options to those listed in Pieces.Color.
    identifier: str                 # A unique identifier used to track pieces.
    points: int                     # The amount of points this piece is worth.
    oneHotEncoding: [int]           # The oneHotEncoding is used for ML purposes.

    def __init__(self, color: Color, identifier: str):
        self.color = color
        self.identifier = identifier
        self.set_points()
        self.oneHotEncoding = generate_one_hot(self.__class__.__name__, self.color)

    @abc.abstractmethod
    def set_points(self) -> None:
        return

    @abc.abstractmethod
    def get_legal_moves(self, pos: Position, game_board: GameBoard) -> PossibleMoveSet:
        """
        This method retrieves the list of legal moves, taking into account the move set of the piece and the board
        and the pieces on it.
        :param pos: :class:`Position` from which the legal have to originate.
        :param game_board: The :class:`GameBoard` that contains all the pieces, needed to determine where a piece
        can and cannot move
        :return: The set of all possible moves and attacks called the :class:`PossibleMoveSet`.
        """
        pass

    def __str__(self):
        """ Overrides the default str method that converts an object to a string"""
        return f"A {self.color} {self.__class__.__name__} worth {self.points} points " \
               f"with one hot encoding {self.oneHotEncoding}"

    @abc.abstractmethod
    def get_letter_code(self) -> chr:
        return

    def is_white(self) -> bool:
        """
        :return: True if the :class:`Piece` is white False otherwise
        """
        return Color.WHITE == self.color

    def is_black(self) -> bool:
        """
        :return: True if the :class:`Piece` is black False otherwise
        """
        return Color.BLACK == self.color


def generate_one_hot(piece_name: str, color: Color) -> [int]:
    """
    Helper function to generate the one-hot-encoding. The index of the 1 is determined and padded with zeroes.
    The total length of the one-hot-encoding is always 12 (0-11).
    :param piece_name: The name of the piece.
    :param color: The color of the piece.
    :return: An array encoding a specific piece and color. Has length 12 with a single one (1) and 11 zeros (0)
    """
    index_dict = {'King': 0, 'Queen': 1, 'Knight': 2, 'Bishop': 3, 'Rook': 4, 'Pawn': 5}
    if color == Color.BLACK:
        base_index = 0
    else:
        base_index = 6

    index = base_index + index_dict[piece_name]
    return [0] * index + [1] + [0] * (11 - index)



