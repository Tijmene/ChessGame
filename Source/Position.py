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

    def to_string(self):
        file = self.get_file()
        rank = self.get_rank()
        return file + str(rank)

    def to_vec(self):
        file = self.get_file()
        vec_x = ord(file) - 65
        vec_y = 8 - (self.get_rank())
        return vec_x, vec_y


def vec_to_pos(vec_x, vec_y):
    file = chr(vec_x + 65)
    rank = 8 - vec_y
    pos = Position(file, rank)
    return pos
