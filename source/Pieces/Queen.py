from source.Pieces.LinearPiece import LinearPiece


class Queen(LinearPiece):

    def get_max_move_len(self) -> int:
        return 7

    def get_move_directions(self) -> [[int]]:
        return [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]

    def set_points(self):
        self.points = 9
        return

    def get_letter_code(self) -> chr:
        return "Q"
