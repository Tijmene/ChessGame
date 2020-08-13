from Source.ChessUtils.Position import Position as Pos
from Source.ChessUtils.Move import Move


class GUIResponse:

    def __init__(self, highlight: Pos = None,
                 possible_moves: [Pos] = None,
                 possible_attacks: [Pos] = None,
                 move: Move = None):

        self.highlight = highlight
        self.possible_moves = possible_moves
        self.possible_attacks = possible_attacks
        self.move = move

    def has_highlight(self):
        return self.highlight is not None

    def has_possible_moves(self):
        return self.possible_moves is not None

    def has_possible_attacks(self):
        return self.possible_attacks is not None

    def has_move(self):
        return self.move is not None
