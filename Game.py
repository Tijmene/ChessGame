from StateBoard import StateBoard
from GUIBoard import GUIBoard
import tkinter as tk
from Position import vec_to_pos


class Game:
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

    def get_game_GUI(self):
        return self.gui_board

    def move_piece(self, prev_pos, new_pos, update_GUI=True):
        self.turn_counter += 1
        self.state_board.move_piece_state(prev_pos, new_pos)
        if update_GUI:
            current_state_board = self.state_board.get_game_state()
            self.gui_board.update_board(current_state_board)

