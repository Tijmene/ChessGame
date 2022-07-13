class Position:
    file: str
    rank: int

    def __init__(self, file, rank):
        self.file = file.upper()
        self.rank = rank

    def get_file(self):
        return self.file

    def get_rank(self):
        return self.rank

    def to_vec(self):
        vec_x = ord(self.file) - 65
        vec_y = 8 - (self.get_rank())
        return vec_x, vec_y

    def __str__(self):
        return "{file}{rank}".format(file=self.file, rank=self.rank)

    def __eq__(self, obj):
        return isinstance(obj, Position) and obj.file == self.file and obj.rank == self.rank


def vec_to_pos(vec_x, vec_y) -> Position:
    file = chr(vec_x + 65)
    rank = 8 - vec_y
    return Position(file, rank)
