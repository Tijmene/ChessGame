from Source.Pieces.Piece import Piece
from Source.ChessUtils.Position import Position as Pos
from Source.ChessUtils.Color import Color


class Pawn(Piece):

    def set_points(self):
        self.points = 1
        return

    def get_possible_moves(self, pos: Pos) -> [Pos]:  # TODO: Implement
        return

    def get_letter_code(self) -> chr:
        return "P"


if __name__ == "__main__":
    testPawn = Pawn(Color.WHITE, Pos("A", 1), "TESTPAWN")
    print(testPawn)