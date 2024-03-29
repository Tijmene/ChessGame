from Chess.Board import GameBoard
from Chess.Pieces.Piece import Piece
from Chess.ChessUtils.Position import Position as Pos, vec_to_pos
from Chess.ChessUtils.PossibleMoveSet import PossibleMoveSet
import numpy as np


class Knight(Piece):
    """
    The knight can hop over other pieces in an L shape move ([1,2] or [2,1])
    """

    def set_points(self) -> None:
        self.points = 3

    def get_legal_moves(self, current_pos: Pos, game_board: GameBoard) -> PossibleMoveSet:
        possible_moves = PossibleMoveSet(current_pos)

        possible_pos_shift = np.array([[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]])
        x, y = current_pos.to_vec()
        np_pos_vec = np.array([x, y])
        shifted_pos = np_pos_vec + possible_pos_shift
        all_actions = []
        for vec_pos in shifted_pos:
            if not np.amin(vec_pos) < 0 and not np.amax(vec_pos) > 7:
                all_actions.append(vec_to_pos(vec_pos[0], vec_pos[1]))

        # Filter the actions
        for action in all_actions:
            content_of_target_square = game_board.square_mapping[action.__str__()]
            if content_of_target_square is None:
                possible_moves.add_move(action)
            elif content_of_target_square.color != self.color:
                possible_moves.add_attack(action)

        return possible_moves

    def get_letter_code(self) -> chr:
        return "N"
