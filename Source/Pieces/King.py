from Source.Pieces.Piece import Piece
from Source.ChessUtils.Position import Position as Pos


class King(Piece):

    def set_points(self):
        self.points = 100
        return

    def get_possible_moves(self) -> [Pos]:  # TODO: Implement
        return

    def get_letter_code(self) -> chr:
        return "K"
