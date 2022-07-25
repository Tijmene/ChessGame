from Chess.ChessUtils.Position import Position


class Move:
    """
    A move consists of a from location (called a position) and a to location
    """
    from_pos: Position
    to_pos: Position
    promoted_to: str

    def __init__(self, from_pos: Position, to_pos: Position, promoted_to: str = ''):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.promoted_to = None if promoted_to == '' else promoted_to

    def __str__(self):
        return f"A move from {self.from_pos} to {self.to_pos}"

    def short_str(self) -> str:
        """
        Method that creates a File Rank string. For instance: MA2A3 or B1C3
        :return: the string representation of the move.
        """
        return f"M{self.from_pos}{self.to_pos}"
