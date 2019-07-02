class Location:
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

class Piece:
    color: chr
    location: Location
    kind: str
    points: int

    def __init__(self, color, start_location, kind):
        self.color = color.upper()
        self.location = start_location
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


kind_dict = {'A': 'R', 'B': 'N', 'C': 'B', 'D': 'Q', 'E': 'K', 'F': 'R', 'G': 'N', 'H': 'B'}


def initial_piece(pos):
    if pos.get_rank() == 2 or pos.get_rank() == 7:
        kind = 'P'
    else:
        kind = kind_dict[pos.get_file()]

    if pos.get_rank() < 3:
        piece = Piece('W', pos, kind)
    elif pos.get_rank() > 6:
        piece = Piece('B', pos, kind)
    else:
        return None
    return piece


def create_game_board():
    initial_board = dict()
    for file in range(65, 73):
        for rank in range(1, 9):
            pos = Location(chr(file), rank)
            initial_board[pos.to_string()] = initial_piece(pos)
    return initial_board


class Game:
    turn_counter: int
    game_board: dict

    def __init__(self):
        self.game_board = create_game_board()

    def get_game_board(self):
        return self.game_board


# def create_move_vector(kind, location):
#     if kind == 'R':
#
#     elif kind == 'K':
#
#     elif kind == 'B':
#
#     elif kind == 'Q':
#
#     elif kind == 'K':
#
#     elif kind == 'P':


new_game = Game()

x = 3
