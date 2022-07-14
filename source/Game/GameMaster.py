import queue
import threading

from source.Board.GUIBoard import GUIBoard
from source.Players.HumanPlayer import HumanPlayer
from source.Players.Player import Player
from source.Board.GameBoard import GameBoard
from source.Clocks.ChessClock import ChessClock
from source.ChessUtils.Move import Move
from source.ChessUtils.Position import Position as Pos
from source.ChessUtils.PossibleMoveSet import PossibleMoveSet
import copy


class GameMaster:
    """
    The top level class of the program. The GameMaster holds all information necessary to run a complete game of
    chess. This GameMaster also takes care of the interaction between :class:`Player`, :class:`GUIBoard`, and itself.
    """

    players: [Player]
    board: GameBoard
    gui: GUIBoard
    clock: ChessClock
    move_inbox: queue.Queue
    game_running: bool = True

    def __init__(self, players: [Player], board: GameBoard, clock: ChessClock, gui_enabled: bool = True) -> None:
        if len(players) != 2:
            raise ValueError("The number of players should be two")

        self.players = players
        self.board = board
        self.clock = clock
        self.move_inbox = queue.Queue()

        if gui_enabled:
            self.gui = GUIBoard(self.board)

    def start(self) -> None:
        """
        Starts the game loop that is executed over and over. The loop updates the :class:`GUIBoard` and checks for new
        instructions from :class:`Player` to :class:`Move` a :class:`Piece` on the :class:`GameBoard`.
        The game master keeps track of the time using the :class:`ChessClock` and is the only entity that has the power
        to move pieces.
        """
        self._connect_players()
        self._start_players()

        self.clock.start()
        self._poke_active_player()

        print("Starting the Chess Game, good luck!")
        self._print_status()

        # This is the main game loop
        while self.game_running:

            # Continuously update the Gui
            self.gui.update()

            # If a move was posted to the game master
            if not self.move_inbox.empty():
                # Retrieve it
                move = self.move_inbox.get()

                # And process it.
                self.board.move_piece(move)
                self.gui.state_update(self.board)

                # Direct the active player to make a move.
                self.clock.switch()
                self._poke_active_player()

                # Print a summary of the game so far
                self._print_status()

        # When the game is no longer running we stop the clock.
        self.clock.stop()

    def _connect_players(self):
        for player in self.players:
            player.move_out_box = self.move_inbox
            self.gui.connect_player(player)

    def _start_players(self):
        for player in self.players:
            threading.Thread(target=player.run).start()

    def _poke_active_player(self) -> None:
        self._get_active_player().inbox.put(self.board)

    def _get_active_player(self) -> Player:
        return self.players[0] if self.players[0].color == self.board.get_active_color() else self.players[1]

    def _print_status(self) -> None:
        print(f"Starting turn {self.board.turn_counter}")
        print(self.clock)
        print(f"{self.board.evaluate()}\n")



