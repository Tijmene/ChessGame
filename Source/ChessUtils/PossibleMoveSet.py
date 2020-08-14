from Source.ChessUtils.Position import Position as Pos


class PossibleMoveSet:

    def __init__(self):
        self.possible_moves = []
        self.possible_attacks = []

    def add_move(self, pos: Pos):
        self.possible_moves.append(pos)

    def add_attack(self, pos: Pos):
        self.possible_attacks.append(pos)
