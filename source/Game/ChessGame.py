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


class ChessGame:
    """ The top level class of the program. The ChessGame holds all information necessary to run a complete game of chess
    This class also takes care of the interaction between player and game """
    players: [Player]
    board: GameBoard
    gui: GUIBoard
    clock: ChessClock
    move_inbox: queue.Queue
    game_running: bool = True

    def __init__(self, players: [Player], board: GameBoard, clock: ChessClock, gui_enabled=True) -> None:
        if len(players) != 2:
            raise ValueError("The number of players should be two")

        self.players = players
        self.board = board
        self.clock = clock
        self.move_inbox = queue.Queue()

        if gui_enabled:
            self.gui = GUIBoard(self.board)

    def start(self) -> None:
        self._connect_players()
        self._start_players()

        self.clock.start()
        self._poke_active_player()

        # This is the main game loop
        while self.game_running:
            self.gui.update()
            if not self.move_inbox.empty():
                move = self.move_inbox.get()
                self.board.move_piece(move)
                self.gui.state_update(self.board)
                self.clock.switch()
                self._poke_active_player()
                print(self.board.evaluate())

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




