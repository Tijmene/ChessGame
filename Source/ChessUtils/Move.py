from Source.ChessUtils.Position import Position as Pos


class Move:
    """ A move consists of a from location (called a position) and a to location"""
    from_pos: Pos
    to_pos: Pos
    promoted_to: str

    def __init__(self, from_pos: Pos, to_pos: Pos, promoted_to: str = ''):
        self.from_pos = from_pos
        self.to_pos = to_pos
        self.promoted_to = None if promoted_to == '' else promoted_to

    def __str__(self):
        return f"A move from {self.from_pos} to {self.to_pos}"

    def short_str(self):
        return f"M{self.from_pos}{self.to_pos}"
