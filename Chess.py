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


def initial_piece(location):
    if location.get_rank() == 2 or location.get_rank() == 7:
        kind = 'P'
    else:
        kind = kind_dict[location.get_file()]

    if location.get_rank() < 3:
        piece = Piece('W', location, kind)
    elif location.get_rank() > 6:
        piece = Piece('B', location, kind)
    else:
        return None
    return piece


class Game:
    turn_counter: int
    game_board: dict

    def __init__(self):
        self.game_board = self.create_game_board()

    def create_game_board(self):
        initial_board = dict()
        for file in range(65, 73):
            for rank in range(1, 9):
                initial_location = Location(chr(file), rank)
                file_rank_key = chr(file) + str(rank)
                initial_board[file_rank_key] = initial_piece(initial_location)
        return initial_board

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
