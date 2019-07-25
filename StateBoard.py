from Position import Position as Pos, vec_to_pos
from Piece import Piece
import numpy as np


class StateBoard:
    state_board: dict

    def __init__(self):
        self.state_board = create_state_board()

    def get_game_state(self):
        return self.state_board

    def query_game_board(self, pos):
        game_board = self.state_board
        string_pos = pos.to_string()
        element = game_board[string_pos]
        return element

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
    def get_legal_moves(self, pos):
        pos_string = pos.to_string()
        piece_to_move = self.state_board[pos_string]
        legal_moves = []
        if piece_to_move is not None:
            if piece_to_move.get_kind() == 'P':
                pass
            if piece_to_move.get_kind() == 'N':
                possible_pos_shift = np.array([[1, 2], [2, 1], [2, -1], [1, -2], [-1, -2], [-2, -1], [-2, 1], [-1, 2]])
                x, y = pos.to_vec()
                pos_vec = np.array([x, y])
                shifted_pos = pos_vec + possible_pos_shift
                pos_inbound = []
                for vec_pos in shifted_pos:
                    if not np.amin(vec_pos) < 0 and not np.amax(vec_pos) > 7:
                        pos_inbound.append(vec_pos)

                for row, col in pos_inbound:
                    pos = vec_to_pos(row, col)
                    element = self.query_game_board(pos)
                    if element is None or not (element.get_color() == piece_to_move.get_color()):
                        legal_moves.append(pos)

            # if piece.get_kind() == 'B':
            #     pass

            if piece_to_move.get_kind() == 'R':
                x, y = pos.to_vec()
                pos_vec = np.array([x, y])
                minus_rank_bool = True
                plus_rank_bool = True
                minus_file_bool = True
                plus_file_bool = True

                for steps in [1, 2, 3, 4, 5, 6, 7]:
                    minus_shifted_rank = pos_vec - np.array([steps, 0])
                    plus_shifted_rank = pos_vec + np.array([steps, 0])
                    minus_shifted_file = pos_vec - np.array([0, steps])
                    plus_shifted_file = pos_vec + np.array([0, steps])

                    if 0 <= minus_shifted_rank[0] < 8 and minus_rank_bool:
                        pos = vec_to_pos(minus_shifted_rank[0], minus_shifted_rank[1])
                        element = self.query_game_board(pos)
                        if element is None:
                            legal_moves.append(pos)
                            pass
                        elif element.get_color() != piece_to_move.get_color():
                            legal_moves.append(pos)
                            minus_rank_bool = False
                        else:
                            minus_rank_bool = False

                    if 0 <= plus_shifted_rank[0] < 8 and plus_rank_bool:
                        pos = vec_to_pos(plus_shifted_rank[0], plus_shifted_rank[1])
                        element = self.query_game_board(pos)
                        if element is None:
                            legal_moves.append(pos)
                        elif element.get_color() != piece_to_move.get_color():
                            legal_moves.append(pos)
                            plus_rank_bool = False
                        else:
                            plus_rank_bool = False

                    if 0 <= minus_shifted_file[1] < 8 and minus_file_bool:
                        pos = vec_to_pos(minus_shifted_file[0], minus_shifted_file[1])
                        element = self.query_game_board(pos)
                        if element is None:
                            legal_moves.append(pos)
                        elif element.get_color() != piece_to_move.get_color():
                            legal_moves.append(pos)
                            minus_file_bool = False
                        else:
                            minus_file_bool = False

                    if 0 <= plus_shifted_file[1] < 8 and plus_file_bool:
                        pos = vec_to_pos(plus_shifted_file[0], plus_shifted_file[1])
                        element = self.query_game_board(pos)
                        if element is None:
                            legal_moves.append(pos)
                        elif element.get_color() != piece_to_move.get_color():
                            legal_moves.append(pos)
                            plus_file_bool = False
                        else:
                            plus_file_bool = False

            # if piece_to_move.get_kind() == 'Q':
            #     pass

            if piece_to_move.get_kind() == 'K':
                x, y = pos.to_vec()
                pos_vec = np.array([x, y])
                possible_pos_shift = np.array([[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]])
                shifted_pos = pos_vec + possible_pos_shift
                pos_inbound = []
                for vec_pos in shifted_pos:
                    if not np.amin(vec_pos) < 0 and not np.amax(vec_pos) > 7:
                        pos_inbound.append(vec_pos)

                for row, col in pos_inbound:
                    pos = vec_to_pos(row, col)
                    element = self.query_game_board(pos)
                    if element is None or not (element.get_color() == piece_to_move.get_color()):
                        legal_moves.append(pos)

        return legal_moves

    def check_move(self, prev_pos, new_pos):
        legal_moves_string = []
        legal_moves = self.get_legal_moves(prev_pos)
        for move in legal_moves:
            move_string = move.to_string()
            legal_moves_string.append(move_string)
        if new_pos.to_string() in legal_moves_string:
            return True
        else:
            return False

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


if __name__ == '__main__':
    test_stateboard = StateBoard()
    test_pos_prev = Pos('A', 1)
    test_pos_new = Pos('A', 5)
    is_legal = test_stateboard.check_move(test_pos_prev, test_pos_new)
