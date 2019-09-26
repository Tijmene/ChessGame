import keras
import tensorflow as tf
import numpy as np


def create_ml_input(state_board):
    state = state_board.get_game_state()
    ml_input = []
    for file in range(65, 73):
        for rank in range(1, 9):
            element = state[chr(file) + str(rank)]
            if element is not None:
                encoding = element.get_one_hot()
            else:
                encoding = [0] * 12
            encoding = np.array(encoding)
            ml_input.append(encoding)
    ml_input = np.array(ml_input)
    return ml_input


def create_ml_input_piece_moved(state_board):
    state = state_board.get_game_state()
    ml_input = []
    for file in range(65, 73):
        for rank in range(1, 9):
            element = state[chr(file) + str(rank)]
            if element is not None:
                encoding = 1
            else:
                encoding = 0
            encoding = np.array(encoding)
            ml_input.append(encoding)
    ml_input = np.array(ml_input)
    return ml_input


