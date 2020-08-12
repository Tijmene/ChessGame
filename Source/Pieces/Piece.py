from Source.ChessUtils.Position import Position as Pos
from Source.Pieces.Color import Color
import abc


class Piece:
    """ The abstract piece class, all functionality that is shared between all pieces is written into this class
    Some methods are labeled with the abstract annotation which means that they have to be implemented by any
    class that inherits from this class"""
    __metaclass__ = abc.ABCMeta     # This declares this class as abstract.
    color: Color                    # An enum class is used to restrict options to those listed in Pieces.Color.
    position: Pos                   # Position as described by the Position class.
    identifier: str                 # An unique identifier used to track pieces.
    points: int                     # The amount of points this piece is worth.
    oneHotEncoding: [int]           # The oneHotEncoding is used for ML purposes.

    def __init__(self, color: Color, start_position: Pos, identifier: str):
        self.color = color
        self.position = start_position
        self.identifier = identifier
        self.set_points()
        self.oneHotEncoding = generate_one_hot(self.__class__.__name__, self.color)

    @abc.abstractmethod
    def set_points(self) -> None:
        return

    def move(self, new_position: Pos) -> bool:
        """ If the new_position is in the list of possible moves of this piece it is moved and True is returned
         If the new_position was not in the list of eligible moves the piece is not moved and False is returned"""
        if new_position in self.get_possible_moves():
            self.position = new_position
            return True
        else:
            return False

    @abc.abstractmethod
    def get_possible_moves(self) -> [Pos]:
        return

    def __str__(self):
        """ Overrides the default str method that convers an object to a string"""
        return "A {color} {type} worth {points} points " \
               "at {pos} with one hot encoding {oneHot}".format(color=self.color,
                                                                type=self.__class__.__name__,
                                                                points=self.points,
                                                                pos=self.position,
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



