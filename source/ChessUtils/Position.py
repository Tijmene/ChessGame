class Position:
    """
    In chess a square is described by a file (letter) and a rank (number). We call this file rank format a Position.
    """
    file: str
    rank: int

    def __init__(self, file, rank):
        self.file = file.upper()
        self.rank = rank

    def get_file(self) -> str:
        """
        Get the file (e.g. A or H) of the position
        :return: the file
        """
        return self.file

    def get_rank(self) -> int:
        """
        Get the rank (e.g. 1 or 5) of the position
        :return: the rank
        """
        return self.rank

    def to_vec(self):
        """
        Vectorize the position
        :return:
        """
        vec_x = ord(self.file) - 65
        vec_y = 8 - (self.get_rank())
        return vec_x, vec_y

    def __str__(self):
        return f"{self.file}{self.rank}"

    def __eq__(self, obj):
        return isinstance(obj, Position) and obj.file == self.file and obj.rank == self.rank


def vec_to_pos(vec_x, vec_y) -> Position:
    """
    Constructor to create a :class:`Position` from a vector.
    :param vec_x: x component of the vector
    :param vec_y: y component of the vector
    :return: :class:`Position` representation of the vector input
    """
    file = chr(vec_x + 65)
    rank = 8 - vec_y
    return Position(file, rank)
