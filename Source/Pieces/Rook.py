from Source.Pieces.LinearPiece import LinearPiece
from Source.Pieces.Piece import Piece
from Source.ChessUtils.Position import Position as Pos, vec_to_pos
from Source.ChessUtils.PossibleMoveSet import PossibleMoveSet
import numpy as np


class Rook(LinearPiece):

    def get_move_vec(self) -> [[int]]:
        return [[0, 1], [1, 0], [0, -1], [-1, 0]]

    def get_max_move_len(self) -> int:
        return 7

    def set_points(self):
        self.points = 5
        return

    def get_letter_code(self) -> chr:
        return "R"
