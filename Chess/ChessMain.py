from Chess.Game.GameMaster import GameMaster
from Chess.Clocks.NoIncrement import NoIncrement
from Chess.Board.GameBoard import GameBoard
from Chess.Players.HumanPlayer import HumanPlayer
from Chess.Players.AIPlayer import AIPlayer
from Chess.ChessUtils.Color import Color


if __name__ == "__main__":
    player_1 = HumanPlayer("Simon", Color.WHITE)
    player_2 = HumanPlayer("Tijmen", Color.BLACK)

    board = GameBoard()
    board.generate_default_setup()

    game_master = GameMaster(players=[player_1, player_2],
                             board=board,
                             clock=NoIncrement(),
                             gui_enabled=True)
    game_master.start()
