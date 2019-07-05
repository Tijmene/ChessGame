import Position


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


def set_points(kind):
    point_dict = {'K': 100, 'Q': 9, 'N': 3, 'B': 3, 'R': 5, 'P': 1}
    return point_dict[kind]