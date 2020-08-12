from StateBoard import StateBoard
from GUIBoard import GUIBoard
from copy import copy, deepcopy
import tkinter as tk
from Position import vec_to_pos


class ChessGame:
    turn_counter: int
    state_board: StateBoard
    gui_board: GUIBoard

    def __init__(self, root, turn_counter=0, GUI=True):
        self.state_board = StateBoard()
        self.turn_counter = turn_counter
        if GUI:
            self.gui_board = GUIBoard(root, self.state_board, self.turn_counter)

    def get_game_state(self):
        return self.state_board

    def get_turn_counter(self):
        return self.turn_counter

    def get_game_GUI(self):
        return self.gui_board

    def move_piece(self, prev_pos, new_pos, update_GUI=True):
        self.turn_counter += 1
        self.state_board.move_piece_state(prev_pos, new_pos)
        if update_GUI:
            current_state_board = self.state_board.get_game_state()
            self.gui_board.update_board(current_state_board)


def construct_possible_state_tree(depth, state, turn_count):
    if depth == 0:
        return None
    else:
        possible_future_states = []
        state_dict = state.get_game_state()
        if turn_count % 2 == 0:
            turn = 'W'
        else:
            turn = 'B'

        # TODO: implement ML function
        # piece_pos_selection = ml_function(state)
        # for piece_pos in piece_pos_selection:
        #     legal_moves = state.get_legal_moves(piece_pos)
        #     for move in legal_moves:
        #         state_copy = deepcopy(state)
        #         state_copy.move_piece_state(piece_pos, move)
        #         sub_worlds = construct_possible_state_tree(depth - 1, state, turn_count + 1)
        #         possible_future_states.append((state_copy, sub_worlds))
        # return possible_future_states

        for piece in state_dict.values():
            if piece is not None and piece.get_color() == turn:
                position = piece.get_position()
                legal_moves = state.get_legal_moves(position)
                for move in legal_moves:
                    state_copy = deepcopy(state)
                    state_copy.move_piece_state(position, move)
                    sub_worlds = construct_possible_state_tree(depth - 1, state, turn_count + 1)
                    possible_future_states.append((state_copy, sub_worlds))
        return possible_future_states
