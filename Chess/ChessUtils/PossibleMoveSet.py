from Chess.ChessUtils.Position import Position


class PossibleMoveSet:
    """
    Set containing all the :class:`Move`s a piece can make, divided in moves and attacks. It also contains the origin
    of all these moves
    """
    from_position: Position
    possible_moves: [Position]
    possible_attacks: [Position]

    def __init__(self, from_position: Position = None):
        self.from_position = from_position
        self.possible_moves = []
        self.possible_attacks = []

    def add_move(self, pos: Position) -> None:
        """
        Add a position to the possible moves of the set
        :param pos: :class:`Position` the position (square) that can be moved to.
        """
        self.possible_moves.append(pos)

    def add_attack(self, pos: Position) -> None:
        """
        Add a position to the attack moves of the set
        :param pos: :class:`Position` the position (square) that can be attacked.
        """
        self.possible_attacks.append(pos)

    def is_empty(self) -> bool:
        """
        Checks if the set is empty
        :return: True if empty False if otherwise.
        """
        return True if self.from_position is None \
                    and len(self.possible_moves) == 0 \
                    and len(self.possible_attacks) == 0 \
                    else False

    def is_not_empty(self) -> bool:
        """
        Checks if the set is not empty
        :return: False if empty True if otherwise.
        """
        return not self.is_empty()

    def __contains__(self, position: Position):
        return position in self.possible_moves or position in self.possible_attacks
