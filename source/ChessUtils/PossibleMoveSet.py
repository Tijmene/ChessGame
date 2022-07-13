from source.ChessUtils.Position import Position as Pos


class PossibleMoveSet:
    from_position: Pos
    possible_moves: [Pos]
    possible_attacks: [Pos]

    """ Set containing all the moves a piece can make, divided in moves and attacks """
    def __init__(self, from_position: Pos = None):
        self.from_position = from_position
        self.possible_moves = []
        self.possible_attacks = []

    def add_move(self, pos: Pos):
        self.possible_moves.append(pos)

    def add_attack(self, pos: Pos):
        self.possible_attacks.append(pos)

    def is_empty(self):
        return True if self.from_position is None \
                    and len(self.possible_moves) == 0 \
                    and len(self.possible_attacks) == 0 \
                    else False

    def is_not_empty(self):
        return not self.is_empty()

    def __contains__(self, position: Pos):
        return position in self.possible_moves or position in self.possible_attacks
