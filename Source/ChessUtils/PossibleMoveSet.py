from Source.ChessUtils.Position import Position as Pos


class PossibleMoveSet:

    def __init__(self, possible_moves: [Pos] = [], possible_attacks: [Pos] = []):
        self.possible_moves = possible_moves
        self.possible_attacks = possible_attacks
