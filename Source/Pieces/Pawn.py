from Source.Pieces.Piece import Piece
from Source.Pieces.Position import Position as Pos
from Source.Pieces.Color import Color


class Pawn(Piece):

    def set_points(self):
        self.points = 1
        return

    def get_possible_moves(self) -> [Pos]:  # TODO: Implement
        return


if __name__ == "__main__":
    testPawn = Pawn(Color.WHITE, Pos("A", 1), "TESTPAWN")
    print(testPawn)