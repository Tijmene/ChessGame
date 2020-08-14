from Source.Pieces.Piece import Piece
from Source.ChessUtils.Position import Position as Pos, vec_to_pos
from Source.ChessUtils.PossibleMoveSet import PossibleMoveSet
import numpy as np


class King(Piece):

    def set_points(self):
        self.points = 100
        return

    def get_legal_moves(self, pos: Pos, square_mapping: dict) -> PossibleMoveSet:  # TODO: Implement
        possible_moves = PossibleMoveSet()


        x, y = pos.to_vec()
        pos_vec = np.array([x, y])
        possible_pos_shift = np.array([[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]])
        shifted_pos = pos_vec + possible_pos_shift
        pos_inbound = []
        for vec_pos in shifted_pos:
            if not np.amin(vec_pos) < 0 and not np.amax(vec_pos) > 7:
                pos_inbound.append(vec_pos)

        for row, col in pos_inbound:
            pos = vec_to_pos(row, col)
            element = square_mapping[pos.__str__()]
            if element is None:
                possible_moves.add_move(pos)
            elif element.color != self.color:
                possible_moves.add_attack(pos)

        return possible_moves

    def get_letter_code(self) -> chr:
        return "K"
