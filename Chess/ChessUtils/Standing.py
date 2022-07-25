class Standing:
    """
    A summary of the points in possession for each color in the chess game.
    """
    black_standing: int
    white_standing: int

    def __init__(self, black_standing, white_standing):
        self.black_standing = black_standing
        self.white_standing = white_standing

    def __str__(self):
        if self.black_standing == self.white_standing:
            return "Both players have equal points!"
        elif self.black_standing > self.white_standing:
            point_lead = self.black_standing - self.white_standing
            return f"Black is leading by {point_lead} point{'s' if point_lead > 1 else ''}!"
        else:
            point_lead = self.white_standing - self.black_standing
            return f"White is leading by {point_lead} point{'s' if point_lead > 1 else ''}!"
