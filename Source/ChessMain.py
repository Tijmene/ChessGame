from Source.Game.ChessGame import ChessGame
from Source.Clocks.NoIncrement import NoIncrement
from Source.Board.GameBoard import GameBoard
from Source.Players.HumanPlayer import HumanPlayer
from Source.Players.AIPlayer import AIPlayer
from Source.ChessUtils.Color import Color


if __name__ == "__main__":
    player_1 = HumanPlayer("Simon", Color.WHITE)
    player_2 = HumanPlayer("Tijmen", Color.BLACK)

    board = GameBoard()
    board.generate_default_setup()

    game = ChessGame(players=[player_1, player_2],
                     board=board,
                     clock=NoIncrement(),
                     gui_enabled=True)
    game.run()
