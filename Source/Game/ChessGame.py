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
    content_previous_click = None

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
        response = GUIResponse()
        if content_clicked_square is not None:
            piece = content_clicked_square
            if piece.is_white() and self.turn_counter % 2 == 1:
                response.highlight = user_input
                (possible_moves, possible_attacks) = self.__generate_legal_actions(user_input)
            elif piece.is_black() and self.turn_counter % 2 == 0:
                response.highlight = user_input
                (possible_moves, possible_attacks) = self.__generate_legal_actions(user_input)
            response.possible_moves = possible_moves
            response.possible_attacks = possible_attacks

        self.q.put(response)

    def __generate_legal_actions(self, user_input: Pos) -> ([Pos], [Pos]):
        possible_moves = []
        possible_attacks = []

        piece = self.board.query(user_input)
        all_actions = piece.get_possible_moves(user_input)
        for action in all_actions:
            content_of_target_square = self.board.query(action.__str__())
            if content_of_target_square is None:
                possible_moves.append(action)
            elif content_of_target_square.color != piece.color:
                possible_attacks.append(action)

        return possible_moves, possible_attacks



