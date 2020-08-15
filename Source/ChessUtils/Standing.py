class Standing:
    black_standing: int
    white_standing: int

    def __init__(self, black_standing, white_standing):
        self.black_standing = black_standing
        self.white_standing = white_standing

    def __str__(self):
        return "Standing: Black has {black_standing} points" \
               ", White has {white_standing} points".format(black_standing=self.black_standing,
                                                            white_standing=self.white_standing)