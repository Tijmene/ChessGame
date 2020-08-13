from Source.Players.Player import Player
from Source.Board.GameBoard import GameBoard
from Source.Clocks.ChessClock import ChessClock
from Source.ChessUtils.Move import Move
from Source.ChessUtils.Position import Position as Pos
from Source.ChessUtils.GUIResponse import GUIResponse
from Source.Pieces.Pawn import Pawn
from Source.Pieces.Knight import Knight
from Source.Pieces.Rook import Rook
from Source.Pieces.Bishop import Bishop
from Source.Pieces.Queen import Queen
from Source.Pieces.King import King

import copy
import queue


class ChessGame:
    """ The top level class of the program. The ChessGame holds all information necesary to run a complete game of chess
    This class also takes care of the interaction between player and game """
    players: [Player]
    turn_counter = 1
    board: GameBoard
    clock: ChessClock
    game_running: bool = True
    last_response_send = GUIResponse()
    last_message_received = None

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
                response = self.__generate_response(user_input)
                if response is not None:
                    self.q.put(response)
                    self.last_response_send = response
                    if response.contains_move():
                        self.clock.switch()
                        self.turn_counter += 1

        self.clock.stop()

    def check_for_user_input(self) -> Pos:
        if self.q.empty():
            return None
        else:
            self.last_message_received = self.q.get()
            return self.last_message_received

    def __generate_response(self, user_input: Pos) -> GUIResponse:
        """ This method checks user input and decides what the necessary action is that should be executed
        If nothing changes (because the users clicks on something irrelevant) the last response is resend"""
        response = GUIResponse()
        piece = self.board.query(user_input)

        # The new input was in the list of possible moves, a move has been made!
        if user_input in self.last_response_send.possible_moves:
            move = Move(self.last_response_send.highlight, user_input)
            self.board.move_piece(move)
            response.move = move

        # The new input was in the list of possible attacks, an enemy piece has been taken!
        elif user_input in self.last_response_send.possible_attacks:
            response.identifier_piece_taken = self.board.query(user_input).identifier
            self.__handle_piece_taken(user_input)
            move = Move(self.last_response_send.highlight, user_input)
            self.board.move_piece(move)
            response.move = move

        # The new input was a square not in the possible moveset. This is either an illegal selection or
        # the selection of a new piece
        elif piece is not None:
            # Check if it was an illegal selection
            if piece.is_white() and self.turn_counter % 2 == 1 or piece.is_black() and self.turn_counter % 2 == 0:
                response.highlight = user_input
                (possible_moves, possible_attacks) = self.__generate_legal_actions(user_input)
                response.possible_moves = possible_moves
                response.possible_attacks = possible_attacks

        # If all checks fail the input is illegal, don't send a response to the GUI
        else:
            response = None
        return response

    def __handle_piece_taken(self, pos: Pos):
        piece = self.board.query(pos)
        points_earned = piece.points
        for player in self.players:
            if piece.is_black() and player.plays_white() or piece.is_white() and player.plays_white():
                player.points_earned += points_earned

    def __generate_legal_actions(self, user_input: Pos) -> ([Pos], [Pos]):
        """ First all actions are retrieved disregarding other pieces on the board. This list of actions
        has to be filtered by the ChessGame class as this class is the only class who has all the information
        to do so and can communicate with the GUI """
        piece = self.board.query(user_input)
        copy_of_game_state = copy.deepcopy(self.board.square_mapping)
        possible_moves, possible_attacks = piece.get_legal_moves(user_input, copy_of_game_state)
        return possible_moves, possible_attacks



