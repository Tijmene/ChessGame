import abc
import copy

from Chess.Board import GameBoard
from Chess.ChessUtils.Position import Position as Pos, vec_to_pos

from Chess.ChessUtils.PossibleMoveSet import PossibleMoveSet
from Chess.Pieces.Piece import Piece


class LinearPiece(Piece):
    """
    All pieces that move in a line (every piece except the Pawn and Knight) inherit from this class.
    """
    __metaclass__ = abc.ABCMeta     # This declares this class as abstract.

    def get_legal_moves(self, from_pos: Pos, game_board: GameBoard) -> PossibleMoveSet:
        possible_moves = PossibleMoveSet(from_pos)
        move_vec_list = self.get_move_directions()
        max_move_len = self.get_max_move_len()

        x, y = from_pos.to_vec()

        for move_modifier in range(1, max_move_len):
            new_move_vec_list = copy.copy(move_vec_list)
            for move_vec in move_vec_list:
                x_moved = x + move_vec[0] * move_modifier
                y_moved = y + move_vec[1] * move_modifier

                target_pos = vec_to_pos(x_moved, y_moved)
                if target_pos.__str__() not in game_board.square_mapping:
                    new_move_vec_list.remove(move_vec)
                    continue

                element = game_board.square_mapping[target_pos.__str__()]
                if element is None:
                    possible_moves.add_move(target_pos)
                elif element.color != self.color:
                    possible_moves.add_attack(target_pos)
                    new_move_vec_list.remove(move_vec)
                elif element.color == self.color:
                    new_move_vec_list.remove(move_vec)

            move_vec_list = new_move_vec_list

        return possible_moves

    @abc.abstractmethod
    def get_move_directions(self) -> [[int]]:
        return None

    @abc.abstractmethod
    def get_max_move_len(self) -> int:
        return None
