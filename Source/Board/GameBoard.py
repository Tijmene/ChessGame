from Source.Pieces.Pawn import Pawn
from Source.Pieces.Bishop import Bishop
from Source.Pieces.King import King
from Source.Pieces.Queen import Queen
from Source.Pieces.Rook import Rook
from Source.Pieces.Knight import Knight

from Source.ChessUtils.Position import Position as Pos
from Source.ChessUtils.Color import Color
from Source.ChessUtils.Move import Move
from Source.Board.GUIBoard import GUIBoard


class GameBoard:
    square_mapping: dict  # A mapping of position strings to chess pieces or empty squares.
    gui_enabled: bool = False
    gui: GUIBoard = None  # The class responsible for creating the Graphical User Interface for the board

    def __init__(self):
        """ Creates an empty board which is a mapping of positions in File Rank format """
        empty_board = dict()
        for file in range(65, 73): # ASCII code for A - H
            for rank in range(1, 9):
                empty_board["{file}{rank}".format(file=chr(file), rank=rank)] = None

        self.square_mapping = empty_board

    def enable_gui(self):
        self.gui_enabled = True

    def generate_default_setup(self):
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

            if rank == "1":
                piece_name = piece_type_dict[file]
                cls = globals()[piece_name]
                self.square_mapping[pos] = cls(color=Color.WHITE,
                                               identifier=pos)

            elif rank == "2":
                self.square_mapping[pos] = Pawn(color=Color.WHITE,
                                                identifier=pos)

            elif rank == "7":
                self.square_mapping[pos] = Pawn(color=Color.BLACK,
                                                identifier=pos)

            elif rank == "8":
                piece_name = piece_type_dict[file]
                cls = globals()[piece_name]
                self.square_mapping[pos] = cls(color=Color.BLACK,
                                               identifier=pos)

    def move_piece(self, move: Move):
        """ Updates the position of a piece on the board """
        piece = self.square_mapping[move.from_pos.__str__()]
        self.square_mapping[move.to_pos.__str__()] = piece
        self.square_mapping[move.from_pos.__str__()] = None

    def draw(self):
        if not self.gui_enabled:
            print("The GUI on this board is switched off, printing string representation \n "
                  "{string_board}".format(string_board=self))
        elif self.gui_enabled and self.gui is None:
            self.gui = GUIBoard(self.square_mapping)
        elif self.gui_enabled and self.gui is not None:
            self.gui.update()

    def __str__(self):
        """ Converts the board to the string representation of the board """
        files = list(range(65, 73))
        ranks = list(range(1, 9))
        ranks.reverse()

        str_output = "CHESS GAME: \n _ _ _ _ _ _ _ _ \n"

        for rank in ranks:  # ASCII code for A - H
            str_output += "|"
            for file in files:
                content = self.square_mapping["{file}{rank}".format(file=chr(file), rank=rank)]
                if content is None:  # Create a checker board pattern with white and black squares.
                    if file % 2 == 0:  # Even file
                        if rank % 2 == 0:
                            str_output += "\u0332 |"
                        else:
                            str_output += "\u0332\u258B|"

                    else:
                        if rank % 2 == 0:
                            str_output += "\u0332\u258B|"
                        else:
                            str_output += "\u0332 |"
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