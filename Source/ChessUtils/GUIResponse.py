from Source.ChessUtils.Position import Position as Pos
from Source.ChessUtils.PossibleMoveSet import PossibleMoveSet
from Source.ChessUtils.Move import Move


class GUIResponse:

    def __init__(self, highlight: Pos = None,
                 possible_move_set: PossibleMoveSet = None,
                 possible_moves: [Pos] = [],
                 possible_attacks: [Pos] = [],
                 move: Move = None,
                 identifier_piece_taken: str = None):

        self.highlight = highlight
        self.possible_move_set = possible_move_set
        self.possible_moves = possible_moves
        self.possible_attacks = possible_attacks
        self.move = move
        self.identifier_piece_taken = identifier_piece_taken

    def contains_highlight(self):
        return self.highlight is not None

    def contains_possible_move_set(self):
        return self.possible_move_set is not None

    def contains_possible_moves(self):
        return self.possible_moves is not None

    def contains_possible_attacks(self):
        return self.possible_attacks is not None

    def contains_move(self):
        return self.move is not None

    def contains_identifier_piece_taken(self):
        return self.identifier_piece_taken is not None
