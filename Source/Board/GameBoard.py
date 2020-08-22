from Source.Pieces.Piece import Piece
from Source.Pieces.Pawn import Pawn
from Source.Pieces.Bishop import Bishop
from Source.Pieces.King import King
from Source.Pieces.Queen import Queen
from Source.Pieces.Rook import Rook
from Source.Pieces.Knight import Knight

from Source.ChessUtils.Position import Position as Pos
from Source.ChessUtils.Color import Color
from Source.ChessUtils.Move import Move
from Source.ChessUtils.Standing import Standing
from Source.Board.GUIBoard import GUIBoard

import numpy as np


class GameBoard:
    square_mapping: dict  # A mapping of position strings to chess pieces or empty squares.
    gui: GUIBoard = None  # The class responsible for creating the Graphical User Interface for the board
    update_str_board = True  # This bool is used to redraw the string representation on updates(if gui is disabled)

    def __init__(self, square_mapping=None):
        """ A board can be initialized with a certain setup or as an empty board """
        if square_mapping is None:
            self.square_mapping = self.__create_empty_board()
        else:
            self.square_mapping = square_mapping

    def enable_gui(self):
        self.gui = GUIBoard(self.square_mapping)

    def connect(self, queue):
        if self.gui is None:
            raise Exception("The GUI is not enabled")
        else:
            self.gui.connect(queue)

    def __create_empty_board(self) -> dict:
        """ Creates an empty board which is a mapping of positions in File Rank format """
        empty_board = dict()
        for file in range(65, 73): # ASCII code for A - H
            for rank in range(1, 9):
                empty_board["{file}{rank}".format(file=chr(file), rank=rank)] = None
        return empty_board

    def generate_default_setup(self):
        """ Populates the board with the initial default chess setup """
        piece_type_dict = {
            **dict.fromkeys(['A', 'H'], 'Rook'),
            **dict.fromkeys(['B', 'G'], 'Knight'),
            **dict.fromkeys(['C', 'F'], 'Bishop'),
            'D': 'Queen',
            'E': 'King'
        }

        for pos in self.square_mapping.keys():
            file = pos[0]
            rank = pos[1]

            if rank == "1" or rank == "2":
                color = Color.WHITE
            elif rank == "7" or rank == "8":
                color = Color.BLACK

            if rank == "2" or rank == "7":
                self.square_mapping[pos] = Pawn(color=color,
                                                identifier=pos)
            elif rank == "1" or rank == "8":
                piece_name = piece_type_dict[file]
                cls = globals()[piece_name]  # Loads the class via the name of the class.
                self.square_mapping[pos] = cls(color=color,
                                               identifier=pos)

    def query(self, pos: Pos) -> Piece:
        """ Queries the board and returns the piece if present, else returns None """
        return self.square_mapping.get(pos.__str__())

    def move_piece(self, move: Move):
        """ Updates the position of a piece on the board """
        piece = self.square_mapping[move.from_pos.__str__()]
        if piece is None:
            raise Exception("Error, there is no square to move on ths position")  # Sanity check
        elif isinstance(piece, Pawn) and piece.check_for_promotion(move=move):  # TODO: change GUI image of pawn to Queen
            self.square_mapping[move.to_pos.__str__()] = Queen(color=piece.color, identifier=piece.identifier)
            self.square_mapping[move.from_pos.__str__()] = None
            self.update_str_board = True
        else:
            self.square_mapping[move.to_pos.__str__()] = piece
            self.square_mapping[move.from_pos.__str__()] = None
            self.update_str_board = True

    def draw(self):
        """ If the GUI is enabled update the GUI. If the GUI is not enabled output
        the string representation of the board"""
        if self.gui is not None:
            self.gui.update()
        elif self.gui is None:
            self.__str_print_on_update()

    def __str_print_on_update(self):
        if self.update_str_board:
            print("The GUI on this board is switched off, printing string representation \n "
                  "{string_board}".format(string_board=self))
            self.update_str_board = False

    def evaluate(self) -> Standing:  # TODO: Improve performance by dict holding only square names with pieces on them
        black_standing = 139  # Total points for a full board.
        white_standing = 139
        for element in self.square_mapping.values():
            if element is not None:
                if element.is_white():
                    black_standing -= element.points
                if element.is_black():
                    white_standing -= element.points

        return Standing(black_standing=black_standing, white_standing=white_standing)

    def to_dnn_input(self) -> np.array:
        """ Creates the input for the Deep Neural network architecture. This method initializes a numpy array,
        loops over every square on a 8x8 board and inserts the oneHotEncoding for each element into the numpy array.
        This creates an output of fixed length 64 * 12 = 768 which can be fed into the Deep Neural Net so that it can
        use it to predict the next move. Only works with 8 by 8 boards """
        dnn_input = []
        one_hot_length = 12
        for file in range(65, 73):
            for rank in range(1, 9):
                square = Pos(chr(file), rank).__str__()
                piece = self.query(square)
                if piece is None:
                    one_hot_encoding = [0] * one_hot_length
                elif piece is not None:
                    one_hot_encoding = piece.oneHotEncoding

                dnn_input.extend(one_hot_encoding)

        return np.array(dnn_input, dtype=int)

    def __str__(self):
        """ Converts the board to the string representation of the board """
        files = list(range(65, 73))
        ranks = list(range(1, 9))
        ranks.reverse()

        str_output = "_ _ _ _ _ _ _ _ \n"

        for rank in ranks:  # ASCII code for A - H
            str_output += "|"
            for file in files:
                content = self.square_mapping["{file}{rank}".format(file=chr(file), rank=rank)]
                if content is None:  # Create a checker board pattern with white and black squares.
                    if file % 2 == 0 and rank % 2 == 0 or file % 2 != 0 and rank % 2 != 0:
                        str_output += "\u0332 |"
                    else:
                        str_output += "\u0332\u258B|"

                else:
                    piece = content
                    letter_code = piece.get_letter_code()
                    if content.is_white():
                        str_output += "\u0332\033[1m" + letter_code + "|"
                    elif content.is_black():
                        str_output += "\u0332" + letter_code + "|"

            str_output += "\n"

        return str_output[:-1]


if __name__ == "__main__":
    board = GameBoard()
    board.generate_default_setup()
    board.move_piece(Move(Pos("E", 2), Pos("E", 4)))
    board.move_piece(Move(Pos("B", 8), Pos("C", 6)))
    print(board)

    dnn_input = board.to_dnn_input()

    pass