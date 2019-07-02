class Piece:
    color: chr
    location: str
    kind: str
    points: int

    def __init__(self, color, start_location, kind):
        self.color = color.upper()
        self.location = start_location.upper()
        self.kind = kind.upper()
        self.points = self.set_points(kind.upper())

    def get_color(self):
        return self.color

    def get_kind(self):
        return self.kind

    def get_location(self):
        return self.location

    def move(self, new_location):
        self.location = new_location

    def set_points(self, kind):
        if kind == 'K':
            return 100
        if kind == 'Q':
            return 9
        if kind == 'N':
            return 3
        if kind == 'B':
            return 3
        if kind == 'R':
            return 5
        if kind == 'P':
            return 1

# rook = Piece('w',"a1",'r')

class GameBoard:
    def __init__(self):
