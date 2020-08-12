from Source.Pieces.Piece import Piece
from Source.Pieces.Position import Position as Pos
from Source.Pieces.Color import Color


class King(Piece):

    def set_points(self):
        self.points = 100
        return

    def get_possible_moves(self) -> [Pos]:  # TODO: Implement
        return