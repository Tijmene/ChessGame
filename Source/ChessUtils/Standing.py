class Standing:
    black_standing: int
    white_standing: int

    def __init__(self, black_standing, white_standing):
        self.black_standing = black_standing
        self.white_standing = white_standing

    def __str__(self):
        return f"Standing: Black has {self.black_standing} point{'s' if self.black_standing != 1  else ''}" \
               f", White has {self.white_standing} point{'s' if self.white_standing != 1 else ''}"
