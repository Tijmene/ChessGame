from Position import Position as Pos
from Piece import Piece


class StateBoard:
    def __init__(self):
        self.state_board = create_state_board()

    def get_game_state(self):
        return self.state_board

    def query_game_board(self, pos):
        game_board = self.state_board
        string_pos = pos.to_string()
        piece = game_board[string_pos]
        return piece

    def move_piece_state(self, prev_pos, new_pos):
        game_board = self.state_board
        new_pos_str = new_pos.to_string()
        prev_pos_str = prev_pos.to_string()
        piece = game_board[prev_pos_str]
        piece.update_position(new_pos)
        self.state_board[prev_pos_str] = None
        self.state_board[new_pos_str] = piece

    # TODO At the moment this is a dummy function, this function should use the stateboard to check if a proposed move
    #  is legal (return True) or illegal (return False)
    def check_move(self, prev_pos, new_pos):
        return True

def create_state_board():
    initial_board = dict()
    for file in range(65, 73):
        for rank in range(1, 9):
            pos = Pos(chr(file), rank)
            initial_board[pos.to_string()] = initial_piece(pos)
    return initial_board


def initial_piece(pos):
    kind_dict = {
        **dict.fromkeys(['A', 'H'], 'R'),
        **dict.fromkeys(['B', 'G'], 'N'),
        **dict.fromkeys(['C', 'F'], 'B'),
        'D': 'Q',
        'E': 'K'
    }
    if pos.get_rank() == 2 or pos.get_rank() == 7:
        kind = 'P'
    else:
        kind = kind_dict[pos.get_file()]

    if pos.get_rank() < 3:
        piece = Piece('W', pos, kind, pos.to_string())
    elif pos.get_rank() > 6:
        piece = Piece('B', pos, kind, pos.to_string())
    else:
        return None
    return piece
