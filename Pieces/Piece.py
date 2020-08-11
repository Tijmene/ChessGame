from Pieces.Position import Position as Pos
from Pieces.Color import Color
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
        self.setPoints()
        self.setOneHotEncoding()

    @abc.abstractmethod
    def setPoints(self) -> None:
        return

    def setOneHotEncoding(self) -> None:
        """ Takes the class name and the color to generate the one hot encoding using a helper function"""
        self.oneHotEncoding = generateOneHot(self.__class__.__name__, self.color)
        return

    def move(self, new_position: Pos) -> bool:
        """ If the new_position is in the list of possible moves of this piece it is moved and True is returned
         If the new_position was not in the list of eligible moves the piece is not moved and False is returned"""
        if new_position in self.getPossibleMoves():
            self.position = new_position
            return True
        else:
            return False

    @abc.abstractmethod
    def getPossibleMoves(self) -> [Pos]:
        return

    def __str__(self):
        """ Overrides the default str method that convers an object to a string"""
        return "A {color} {type} worth {points} points at {pos}".format(color=self.color,
                                                                        type=self.__class__.__name__,
                                                                        points=self.points,
                                                                        pos=self.position)


def generateOneHot(kind: str, color: Color) -> [int]:
    """ Helper function to generate the one-hot-encoding. The index of the 1 is determined and padded with zeroes.
    The total length of the one-hot-encoding is always 12 (0-11). """
    index_dict = {'King': 0, 'Queen': 1, 'Knight': 2, 'Bishop': 3, 'Rook': 4, 'Pawn': 5}
    if color == Color.BLACK:
        base_index = 0
    elif color == Color.WHITE:
        base_index = 6

    index = base_index + index_dict[kind]
    return [0] * index + [1] + [0] * (11 - index)



