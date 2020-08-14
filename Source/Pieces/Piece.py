from Source.ChessUtils.Position import Position as Pos
from Source.ChessUtils.Color import Color
from Source.ChessUtils.PossibleMoveSet import PossibleMoveSet
import abc


class Piece:
    """ The abstract piece class, all functionality that is shared between all pieces is written into this class
    Some methods are labeled with the abstract annotation which means that they have to be implemented by any
    class that inherits from this class"""
    __metaclass__ = abc.ABCMeta     # This declares this class as abstract.
    color: Color                    # An enum class is used to restrict options to those listed in Pieces.Color.
    identifier: str                 # An unique identifier used to track pieces.
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
    def get_legal_moves(self, pos: Pos, square_mapping: dict) -> PossibleMoveSet:
        """ This method retrieves the list of legal moves, taking into account the move set of the piece and the board
        and the pieces on it. """
        return

    def __str__(self):
        """ Overrides the default str method that convers an object to a string"""
        return "A {color} {type} worth {points} points " \
               "with one hot encoding {oneHot}".format(color=self.color,
                                                       type=self.__class__.__name__,
                                                       points=self.points,
                                                       oneHot=self.oneHotEncoding)

    @abc.abstractmethod
    def get_letter_code(self) -> chr:
        return

    def is_white(self) -> bool:
        return Color.WHITE == self.color

    def is_black(self) -> bool:
        return Color.BLACK == self.color


def generate_one_hot(kind: str, color: Color) -> [int]:
    """ Helper function to generate the one-hot-encoding. The index of the 1 is determined and padded with zeroes.
    The total length of the one-hot-encoding is always 12 (0-11). """
    index_dict = {'King': 0, 'Queen': 1, 'Knight': 2, 'Bishop': 3, 'Rook': 4, 'Pawn': 5}
    if color == Color.BLACK:
        base_index = 0
    elif color == Color.WHITE:
        base_index = 6

    index = base_index + index_dict[kind]
    return [0] * index + [1] + [0] * (11 - index)



