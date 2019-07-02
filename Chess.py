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

# rook = Piece('w',"A1",'r')

kind_dict = {'A':'R','B':'N','C':'B','D':'Q','E':'K','F':'R','G':'N','H':'B'}

def initial_piece(file_rank):
    if int(file_rank[1]) == 2 or int(file_rank[1]) == 7:
        kind = 'P'
    else:
        kind = kind_dict[file_rank[0]]

    if int(file_rank[1])<3:
        piece = Piece('W' , file_rank, kind)
    elif int(file_rank[1])>6:
        piece = Piece('B' , file_rank, kind)
    else:
        return None
    return piece


class Game:
    turn_counter: int

    def __init__(self):
        self.game_board = self.create_game_board()

    def create_game_board(self):
        initial_board = dict()
        for file in range(65,73):
            for rank in range(1,9):
                file_rank = chr(file) + str(rank)
                initial_board[file_rank] = initial_piece(file_rank)
        return initial_board

    def get_game_board(self):
        return self.game_board


new_game = Game()