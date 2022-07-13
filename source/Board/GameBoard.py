from source.Pieces.Piece import Piece    # Don't remove, needed for image loading
from source.Pieces.Pawn import Pawn      # Don't remove, needed for image loading
from source.Pieces.Bishop import Bishop  # Don't remove, needed for image loading
from source.Pieces.King import King      # Don't remove, needed for image loading
from source.Pieces.Queen import Queen    # Don't remove, needed for image loading
from source.Pieces.Rook import Rook      # Don't remove, needed for image loading
from source.Pieces.Knight import Knight  # Don't remove, needed for image loading
from source.ChessUtils.Position import Position as Pos
from source.ChessUtils.Color import Color
from source.ChessUtils.Move import Move
from source.ChessUtils.Standing import Standing

import numpy as np


class GameBoard:
    square_mapping: dict  # A mapping of position strings to chess pieces or empty squares.
    black_king_moved: bool  # Used for castling.
    white_king_moved: bool  # Used for castling.
    turn_counter: int

    def __init__(self, square_mapping=None):
        """ A board can be initialized with a certain setup or as an empty board (default) """
        if square_mapping is None:
            self.square_mapping = self._create_empty_board()
        else:
            self.square_mapping = square_mapping

        self.turn_counter = 1

    def _create_empty_board(self) -> dict:
        """ Creates an empty board which contains all 64 positions in File Rank format """
        empty_board = dict()
        for file in range(65, 73):  # ASCII code for files A - H
            for rank in range(1, 9):  # Ranks are 1 - 8
                empty_board[f"{chr(file)}{rank}"] = None
        return empty_board

    def generate_default_setup(self):
        """ Populates the board with the initial standard chess setup """
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

            color = Color.WHITE if rank == "1" or rank == "2" else Color.BLACK

            if rank == "2" or rank == "7":
                self.square_mapping[pos] = Pawn(color=color,
                                                identifier=pos)
            elif rank == "1" or rank == "8":
                piece_name = piece_type_dict[file]
                cls = globals()[piece_name]  # Loads the class via the name of the class.
                self.square_mapping[pos] = cls(color=color,
                                               identifier=pos)

    def query(self, pos: Pos) -> Piece:
        """ Queries a square of the board and returns the piece if present, else returns None """
        return self.square_mapping.get(pos.__str__())

    def get_active_color(self) -> Color:
        """
        Gets the color of the player that is supposed to make the next move.
        """
        return Color.BLACK if self.turn_counter % 2 == 0 else Color.WHITE

    def move_piece(self, move: Move):
        """ Updates the position of a piece on the board """
        piece = self.square_mapping[move.from_pos.__str__()]
        if piece is None:
            raise Exception(f"Error, there is no piece on square {move.from_pos} to move.")  # Sanity check
        elif move.promoted_to:
            promoted_piece_name = move.promoted_to
            cls = globals()[promoted_piece_name]  # Loads the class via the name of the class.
            piece = cls(color=piece.color, identifier=piece.identifier)

        self.square_mapping[move.to_pos.__str__()] = piece
        self.square_mapping[move.from_pos.__str__()] = None
        self.turn_counter += 1

    def evaluate(self) -> Standing:  # TODO: Improve performance by dict holding only square names with pieces on them
        black_standing = 0
        white_standing = 0
        for piece in self.square_mapping.values():
            if piece is not None:
                if piece.is_white():
                    white_standing += piece.points
                if piece.is_black():
                    black_standing += piece.points

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
                content = self.square_mapping[f"{chr(file)}{rank}"]
                if content is None:  # Create a checkerboard pattern with white and black squares.
                    if file % 2 == 0 and rank % 2 == 0 or file % 2 != 0 and rank % 2 != 0:
                        str_output += "\u0332 |"
                    else:
                        str_output += "\u0332\u258B|"

                else:
                    piece = content
                    letter_code = piece.get_letter_code()
                    if piece.is_white():
                        str_output += "\u0332\033[1m" + letter_code + "|"
                    elif piece.is_black():
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
    