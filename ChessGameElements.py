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
        rank = self.get_rank() - 1
        vec_file = ord(file) - 65
        return rank, vec_file


class Piece:
    color: chr
    Position: Position
    kind: str
    points: int

    def __init__(self, color, start_position, kind):
        self.color = color.upper()
        self.position = start_position
        self.kind = kind.upper()
        self.points = set_points(kind.upper())

    def get_color(self):
        return self.color

    def get_kind(self):
        return self.kind

    def get_position(self):
        return self.position

    def move(self, new_position):
        self.position = new_position


def set_points(kind):
    point_dict = {'K': 100, 'Q': 9, 'N': 3, 'B': 3, 'R': 5, 'P': 1}
    return point_dict[kind]


kind_dict = dict(A='R', B='N', C='B', D='Q', E='K', F='B', G='N', H='R')


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
            pos = Position(chr(file), rank)
            initial_board[pos.to_string()] = initial_piece(pos)
    return initial_board


class Game:
    turn_counter: int
    game_board: dict

    def __init__(self):
        self.game_board = create_game_board()

    def get_game_board(self):
        return self.game_board

    def query_game_board(self, pos):
        game_board = self.game_board
        string_pos = pos.to_string()
        return game_board[string_pos]


# def create_move_vector(kind, position):
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

if __name__ == "__main__":
    new_game = Game()

    pos = Position('A',1)
    x = new_game.query_game_board(pos)

