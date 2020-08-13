from Source.Pieces.Piece import Piece
from Source.ChessUtils.Position import Position as Pos, vec_to_pos
import numpy as np


class Bishop(Piece):

    def set_points(self):
        self.points = 3
        return

    def get_legal_moves(self, pos: Pos, square_mapping: dict) -> ([Pos], [Pos]):  # TODO: Implement
        possible_moves = []
        possible_attacks = []

        x, y = pos.to_vec()
        pos_vec = np.array([x, y])
        plus_file_plus_rank_bool = True
        plus_file_minus_rank_bool = True
        minus_file_plus_rank_bool = True
        minus_file_minus_rank_bool = True
        bishop_bool = [plus_file_plus_rank_bool, plus_file_minus_rank_bool, minus_file_plus_rank_bool,
                       minus_file_minus_rank_bool]

        for steps in [1, 2, 3, 4, 5, 6, 7]:
            all_directions = pos_vec + np.array([[steps, steps], [steps, -steps], [-steps, steps], [-steps, -steps]])
            for directions in [0, 1, 2, 3]:
                if 0 <= all_directions[directions, 0] < 8 and 0 <= all_directions[directions, 1] < 8 \
                                                          and bishop_bool[directions]:
                    pos = vec_to_pos(all_directions[directions, 0], all_directions[directions, 1])
                    element = square_mapping[pos.__str__()]
                    if element is None and bishop_bool[directions]:
                        possible_moves.append(pos)
                        pass
                    elif element.color != self.color:
                        possible_attacks.append(pos)
                        bishop_bool[directions] = False
                    else:
                        bishop_bool[directions] = False

        return possible_moves, possible_attacks

    def get_letter_code(self) -> chr:
        return "B"
