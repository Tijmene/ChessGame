from Position import Position as Pos, vec_to_pos


class Piece:
    color: chr
    position: Position
    kind: str
    points: int
    name: str

    def __init__(self, color, start_position, kind, name):
        self.color = color.upper()
        self.position = start_position
        self.kind = kind.upper()
        self.points = set_points(kind.upper())
        self.name = name
        self.one_hot_encoding = set_one_hot(kind, color)

    def get_color(self):
        return self.color

    def get_kind(self):
        return self.kind

    def get_position(self):
        return self.position

    def get_name(self):
        return self.name

    def update_position(self, new_position):
        self.position = new_position

    def get_one_hot(self):
        return self.one_hot_encoding

    def get_points(self):
        return self.points


def set_points(kind):
    point_dict = {'K': 1000, 'Q': 90, 'N': 30, 'B': 30, 'R': 50, 'P': 10}
    return point_dict[kind]


def set_one_hot(kind, color):
    n = 0
    index_dict = {'K': 0, 'Q': 1, 'N': 2, 'B': 3, 'R': 4, 'P': 5}
    if color == 'W':
        n += 6
    n += index_dict[kind]
    return [0] * n + [1] + [0] * (11 - n)



