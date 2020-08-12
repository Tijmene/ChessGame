from Source.Pieces.Pawn import Pawn
from Source.ChessUtils.Color import Color
from Source.ChessUtils.Position import Position as Pos


class GameBoard:
    square_mapping: dict # A mapping of position strings to chess pieces or empty squares.

    def __init__(self):
        """ Creates an empty board which is a mapping of positions in File Rank format """
        empty_board = dict()
        for file in range(65, 73): # ASCII code for A - H
            for rank in range(1, 9):
                empty_board["{file}{rank}".format(file=chr(file), rank=rank)] = None

        self.square_mapping = empty_board

    def generate_default_setup(self):
        piece_type = {
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
                piece_name = piece_type[file]
                cls = globals()[piece_name]
                self.square_mapping[pos] = cls(color=Color.WHITE,
                                               start_position=Pos(file, rank),
                                               identifier=pos)

            elif rank == "2":
                self.square_mapping[pos] = Pawn(color=Color.WHITE,
                                                start_position=Pos(file, rank),
                                                identifier=pos)

            elif rank == "7":
                self.square_mapping[pos] = Pawn(color=Color.BLACK,
                                                start_position=Pos(file, rank),
                                                identifier=pos)

            elif rank == "8":
                piece_name = piece_type[file]
                cls = globals()[piece_name]
                self.square_mapping[pos] = cls(color=Color.BLACK,
                                               start_position=Pos(file, rank),
                                               identifier=pos)

    def __str__(self):
        files = list(range(65, 73))
        # files.reverse()
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
    print(board)
