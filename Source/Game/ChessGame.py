from Source.Players.Player import Player
from Source.Board.GameBoard import GameBoard
from Source.Clocks.ChessClock import ChessClock
from Source.ChessUtils.Move import Move
from Source.ChessUtils.Position import Position as Pos
from Source.ChessUtils.GUIResponse import GUIResponse


import queue


class ChessGame:
    """ The top level class of the program. The ChessGame holds all information necesary to run a complete game of chess
    This class also takes care of the interaction between player and game """
    players: [Player]
    turn_counter = 1
    board: GameBoard
    clock: ChessClock
    game_running: bool = True

    def __init__(self, players: [Player], board: GameBoard, clock: ChessClock, gui_enabled=True):
        self.players = players
        self.board = board
        self.clock = clock

        if gui_enabled:
            board.enable_gui()
            self.q = queue.Queue()
            board.connect(queue=self.q)

    def run(self):
        self.clock.start()

        # The main game loop executes here
        while self.game_running:
            self.board.draw()
            user_input = self.check_for_user_input()
            if user_input is not None:
                self.handle_user_input(user_input)

        self.clock.stop()

    def check_for_user_input(self) -> Pos:
        if self.q.empty():
            return None
        else:
            return self.q.get()

    def handle_user_input(self, user_input: Pos):
        """ This method checks user input and decides what the necessary action is that should be executed """
        content_clicked_square = self.board.query(user_input)
        response = None
        if content_clicked_square is not None:
            piece = content_clicked_square
            if piece.is_white() and self.turn_counter % 2 == 1:
                response = (GUIResponse(highlight=user_input))
            elif piece.is_black() and self.turn_counter % 2 == 0:
                response = (GUIResponse(highlight=user_input))

        self.q.put(response)



