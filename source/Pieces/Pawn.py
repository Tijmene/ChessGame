from source.Board import GameBoard
from source.Pieces.Piece import Piece
from source.ChessUtils.Position import Position as Pos, vec_to_pos
from source.ChessUtils.PossibleMoveSet import PossibleMoveSet
from source.ChessUtils.Color import Color
from source.ChessUtils.Move import Move


class Pawn(Piece):
    """ The Pawn can only move forward. """

    def set_points(self):
        self.points = 1
        return

    def check_for_promotion(self, move: Move) -> bool:
        rank = move.to_pos.get_rank()
        if self.is_black() and rank == 1 or self.is_white() and rank == 8:
            return True
        else:
            return False

    def get_legal_moves(self, from_pos: Pos, game_board: GameBoard) -> PossibleMoveSet:  # TODO: Implement
        possible_moves = PossibleMoveSet(from_pos)

        x, y = from_pos.to_vec()

        if self.color == Color.BLACK:
            y1 = y + 1
            if y1 >= 7:
                pass
            move_pos = vec_to_pos(x, y1)
            for i in [-1, 1]:
                if 0 <= x + i < 8:
                    move_pos_capture = vec_to_pos((x + i), y1)
                    element = game_board.square_mapping[move_pos_capture.__str__()]
                    if element is not None and element.color != self.color:
                        possible_moves.add_attack(move_pos_capture)
            if y == 1:
                y2 = y + 2
                move_pos2 = vec_to_pos(x, y2)
                element = game_board.square_mapping[move_pos2.__str__()]


                if element is None:
                    possible_moves.add_move(move_pos2)

        elif self.color == Color.WHITE:
            if y == 6:
                y2 = y - 2
                move_pos2 = vec_to_pos(x, y2)
                element = game_board.square_mapping[move_pos2.__str__()]
                if element is None:
                    possible_moves.add_move(move_pos2)
            y1 = y - 1
            move_pos = vec_to_pos(x, y1)
            for i in [-1, 1]:
                if 0 <= x + i < 8:
                    move_pos_capture = vec_to_pos((x + i), (y - 1))
                    element = game_board.square_mapping.get(move_pos_capture.__str__())
                    if element is not None and element.color != self.color:
                        possible_moves.add_attack(move_pos_capture)

        element = game_board.square_mapping.get(move_pos.__str__())
        if element is None:
            possible_moves.add_move(move_pos)

        return possible_moves

    def get_letter_code(self) -> chr:
        return "P"


if __name__ == "__main__":
    testPawn = Pawn(Color.WHITE, Pos("A", 1), "TESTPAWN")
    print(testPawn)
