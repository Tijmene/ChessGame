from Chess.Pieces.LinearPiece import LinearPiece


class Rook(LinearPiece):

    def get_move_directions(self) -> [[int]]:
        return [[0, 1], [1, 0], [0, -1], [-1, 0]]

    def get_max_move_len(self) -> int:
        return 7

    def set_points(self):
        self.points = 5
        return

    def get_letter_code(self) -> chr:
        return "R"
