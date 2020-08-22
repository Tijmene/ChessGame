from Source.Players.Player import Player
from Source.Board.GameBoard import GameBoard
from Source.Clocks.ChessClock import ChessClock
from Source.ChessUtils.Move import Move
from Source.ChessUtils.Position import Position as Pos
from Source.ChessUtils.GUIResponse import GUIResponse
from Source.ChessUtils.PossibleMoveSet import PossibleMoveSet
import copy
import queue
import time


class ChessGame:
    """ The top level class of the program. The ChessGame holds all information necesary to run a complete game of chess
    This class also takes care of the interaction between player and game """
    players: [Player]
    turn_counter = 1
    board: GameBoard
    clock: ChessClock
    game_running: bool = True
    last_response_send = GUIResponse()

    def __init__(self, players: [Player], board: GameBoard, clock: ChessClock, gui_enabled=True):
        self.players = players
        self.board = board
        self.clock = clock

        if gui_enabled:
            board.enable_gui()
            self.q = queue.Queue()
            board.connect(queue=self.q)

        else:
            self.q = None;

    def run(self):
        self.clock.start()

        # This is the main game loop
        while self.game_running:
            self.board.draw()
            move = self.__get_active_players_move()

            # A move was generated, update and send it to the GUI
            if move is not None:
                self.__send_move_to_gui(move)
                self.clock.switch()
                self.turn_counter += 1
                print(self.board.evaluate())

        self.clock.stop()

    def __get_active_players_move(self) -> Move:
        # Direct the active player to make a move
        for player in self.players:
            if player.plays_black() and self.turn_counter % 2 == 0 \
                    or player.plays_white() and self.turn_counter % 2 == 1:
                move = player.get_next_move(self.board)

        # If no move was generated it means that this is a human player and the move should be retrieved from the GUI
        if move is None:
            move = self.__communicate_with_gui()  # TODO; let player class implement this?

        return move

    def __communicate_with_gui(self) -> Move:
        """ Communicates with the GUI, if this communication leads to the generation of a
        move, this move is returned. """
        user_input = self.__check_for_user_input()
        if user_input is not None:
            response = self.__generate_response(user_input)
            if response is None:
                return None
            elif response.contains_move():
                return response.move
            else:
                self.q.put(response)
                self.last_response_send = response
                return None
        else:
            return None

    def __check_for_user_input(self) -> Pos:
        if self.q.empty():
            return None
        else:
            return self.q.get()

    def __generate_response(self, user_input: Pos) -> GUIResponse:
        """ This method checks user input and decides what the necessary action is that should be executed
        If nothing changes (because the users clicks on something irrelevant) no response is send which causes
        the GUI to remain the same"""
        response = GUIResponse()
        piece = self.board.query(user_input)

        # If the last response send contained a move set it is possible that a piece has been moved
        if self.last_response_send.contains_possible_move_set():
            # The new input was in the list of possible moves, a move has been made!
            if user_input in self.last_response_send.possible_move_set.possible_moves:
                move = Move(self.last_response_send.highlight, user_input)
                response.move = move
                return response

            # The new input was in the list of possible attacks, an enemy piece has been taken!
            elif user_input in self.last_response_send.possible_move_set.possible_attacks:
                response.identifier_piece_taken = self.board.query(user_input).identifier
                self.__handle_piece_taken(user_input)
                move = Move(self.last_response_send.highlight, user_input)
                response.move = move
                return response

        # The new input was not a square not in the possible moveset. The user input is either an illegal selection or
        # the selection of a new piece
        if piece is not None:
            # Highlight the piece is it is the same color as the color of the player who's turn it is
            if piece.is_white() and self.turn_counter % 2 == 1 or piece.is_black() and self.turn_counter % 2 == 0:
                response.highlight = user_input
                response.possible_move_set = self.__generate_legal_actions(user_input)
                return response

        # If all checks fail the input is illegal, don't send a response to the GUI
        else:
            response = None
            return response

    def __handle_piece_taken(self, pos: Pos):
        piece_taken = self.board.query(pos)
        points_earned = piece_taken.points
        for player in self.players:
            if (piece_taken.is_black() and player.plays_white()) or (piece_taken.is_white() and player.plays_black()):
                player.points_earned += points_earned

    def __generate_legal_actions(self, user_input: Pos) -> PossibleMoveSet:
        """ First all actions are retrieved disregarding other pieces on the board. This list of actions
        has to be filtered by the ChessGame class as this class is the only class who has all the information
        to do so and can communicate with the GUI """
        piece = self.board.query(user_input)
        copy_of_game_state = copy.deepcopy(self.board.square_mapping)
        return piece.get_legal_moves(user_input, copy_of_game_state)

    def __send_move_to_gui(self, move: Move):
        gui_message = GUIResponse(move=move)
        piece = self.board.query(move.to_pos)

        # If there was a piece in the target square (to_pos) this piece has been taken.
        if piece is not None:
            gui_message.identifier_piece_taken = piece.identifier

        self.board.move_piece(move)
        self.q.put(gui_message)
        self.last_response_send = gui_message





