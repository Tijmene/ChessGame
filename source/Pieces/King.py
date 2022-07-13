from source.Pieces.LinearPiece import LinearPiece


class King(LinearPiece):

    def get_move_directions(self) -> [[int]]:
        return [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]

    def get_max_move_len(self) -> int:
        return 2

    def set_points(self):
        self.points = 100
        return

    def get_letter_code(self) -> chr:
        return "K"
