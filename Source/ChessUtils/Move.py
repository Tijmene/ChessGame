from Source.ChessUtils.Position import Position as Pos


class Move:
    """ A move consists of a from and a to position"""
    from_pos: Pos
    to_pos: Pos

    def __init__(self, from_pos: Pos, to_pos: Pos):
        self.from_pos = from_pos
        self.to_pos = to_pos

    def __str__(self):
        return "A move from {from_pos} to {to_pos}".format(from_pos=self.from_pos, to_pos=self.to_pos)

    def short_str(self):
        return "M{from_pos}{to_pos}".format(from_pos=self.from_pos, to_pos=self.to_pos)