from source.Game.GameMaster import GameMaster
from source.Clocks.NoIncrement import NoIncrement
from source.Board.GameBoard import GameBoard
from source.Players.HumanPlayer import HumanPlayer
from source.Players.AIPlayer import AIPlayer
from source.ChessUtils.Color import Color


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
