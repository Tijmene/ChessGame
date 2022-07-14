from source.Board.GameBoard import GameBoard
from source.ChessUtils.Position import Position
from source.ChessUtils.PossibleMoveSet import PossibleMoveSet


def generate_moves(game_board: GameBoard,
                   clicked_position: Position) -> PossibleMoveSet:
    """ Generates all the possible moves from a clicked position on the chess board
    :param game_board: :class:`Gameboard` that contains all the necessary information to calculate possible moves
    :param clicked_position: :class:`Position` the position (square) from which all possible moves have to be calculated
    :return: The :class:`PossibleMoveSet` which contains all possible moves and attacks from a square.
    """
    piece = game_board.query(clicked_position)

    # No piece is present on the clicked square, we return the still empty PossibleMoveSet
    if piece is None:
        return PossibleMoveSet()

    # If a piece is clicked that does not belong to the active player we return the still empty PossibleMoveSet
    elif piece.is_white() and game_board.turn_counter % 2 == 0 or piece.is_black() and game_board.turn_counter % 2 == 1:
        return PossibleMoveSet()

    # A piece is clicked that belongs to the active player.
    else:
        return piece.get_legal_moves(clicked_position, game_board)
