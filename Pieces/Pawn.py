from Pieces.Piece import Piece
from Pieces.Position import Position as Pos
from Pieces.Color import Color


class Pawn(Piece):

    def setPoints(self):
        self.points = 10
        return

    def getPossibleMoves(self) -> [Pos]:
        return


if __name__ == "__main__":
    testPawn = Pawn(Color.WHITE, Pos("A", 1), "TESTPAWN")
    print(testPawn)