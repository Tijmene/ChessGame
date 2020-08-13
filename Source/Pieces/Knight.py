from Source.Pieces.Piece import Piece
from Source.ChessUtils.Position import Position as Pos, vec_to_pos
import numpy as np


class Knight(Piece):

    def set_points(self):
        self.points = 3
        return

    def get_possible_moves(self, pos: Pos) -> [Pos]:  # TODO: Implement
        possible_pos_shift = np.array([[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]])
        x, y = pos.to_vec()
        np_pos_vec = np.array([x, y])
        shifted_pos = np_pos_vec + possible_pos_shift
        all_actions = []
        for vec_pos in shifted_pos:
            if not np.amin(vec_pos) < 0 and not np.amax(vec_pos) > 7:
                all_actions.append(vec_to_pos(vec_pos[0], vec_pos[1]))

        return all_actions

    def get_letter_code(self) -> chr:
        return "N"
