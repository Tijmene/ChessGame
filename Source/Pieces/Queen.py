from Source.Pieces.Piece import Piece
from Source.Pieces.Position import Position as Pos
from Source.Pieces.Color import Color


class Queen(Piece):

    def set_points(self):
        self.points = 9
        return

    def get_possible_moves(self) -> [Pos]:  # TODO: Implement
        return
