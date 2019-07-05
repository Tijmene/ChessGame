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
        vec_rank = self.get_rank() - 1
        vec_file = ord(file) - 65
        return vec_rank, vec_file