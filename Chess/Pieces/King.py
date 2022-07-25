from Chess.Pieces.LinearPiece import LinearPiece


class King(LinearPiece):
    """
    The King who can move in all directions but can only take a single step
    """

    def get_move_directions(self) -> [[int]]:
        return [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]

    def get_max_move_len(self) -> int:
        return 2

    def set_points(self) -> None:
        self.points = 100

    def get_letter_code(self) -> chr:
        return "K"
