from Chess.Pieces.LinearPiece import LinearPiece


class Bishop(LinearPiece):
    """
    The bishop who can only move diagonally
    """

    def get_move_directions(self) -> [[int]]:
        return [[1, 1], [1, -1], [-1, -1], [-1, 1]]

    def get_max_move_len(self) -> int:
        return 7

    def set_points(self) -> None:
        self.points = 3

    def get_letter_code(self) -> chr:
        return "B"
