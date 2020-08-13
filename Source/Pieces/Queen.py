from Source.Pieces.Piece import Piece
from Source.ChessUtils.Position import Position as Pos


class Queen(Piece):

    def set_points(self):
        self.points = 9
        return

    def get_legal_moves(self, pos: Pos, square_mapping: dict) -> ([Pos], [Pos]):  # TODO: Implement
        return

    def get_letter_code(self) -> chr:
        return "Q"
