from Source.Pieces.LinearPiece import LinearPiece
from Source.ChessUtils.Position import Position as Pos, vec_to_pos
from Source.ChessUtils.PossibleMoveSet import PossibleMoveSet
import numpy as np


class King(LinearPiece):

    def get_move_directions(self) -> [[int]]:
        return [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]

    def get_max_move_len(self) -> int:
        return 2

    def set_points(self):
        self.points = 100
        return

    def get_letter_code(self) -> chr:
        return "K"
