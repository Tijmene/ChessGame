from Source.Game.ChessGame import ChessGame
from Source.Clocks.NoIncrement import NoIncrement
from Source.Board.GameBoard import GameBoard
from Source.Players.HumanPlayer import HumanPlayer


if __name__ == "__main__":
    player_1 = HumanPlayer("Simon")
    player_2 = HumanPlayer("Tijmen")

    board = GameBoard(gui_enabled=False)
    board.generate_default_setup()

    game = ChessGame(players=[player_1, player_2],
                     board=board,
                     clock=NoIncrement())
    game.run()
