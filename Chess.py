class Piece:
    def __init__(self, color, start_location, kind):
        self.color = color
        self.location = start_location
        self.kind = kind

    def get_color(self):
        return self.color

    def get_location(self):
        return self.location

    def move(self, new_location):
        self.location = new_location


rook = Piece('w',)

currentPos = rook.get_location()

class GameBoard:
    def __init__(self):
