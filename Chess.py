class Piece:
    def __init__(self, color, start_location, kind):
        self.color = color
        self.location = start_location
        self.kind = kind
    def show(self):
        print(self.color)

    def move(self,new_location):
        self.location = new_location

    def change_side(self):
        if self.color == 'b':
            self.color = 'w'
        else:
            self.color = 'b'


