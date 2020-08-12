from Source.Players.Player import Player
from Source.Board.GameBoard import GameBoard
from Source.Clocks.ChessClock import ChessClock
from Source.ChessUtils.Move import Move


class ChessGame:
    """ The top level class of the program. The ChessGame holds all information necesary to run a complete game of chess
    This class also takes care of the interaction between player and game """
    players: [Player]
    turn_counter = 1
    board: GameBoard
    clock: ChessClock
    game_running: bool = True

    def __init__(self, players: [Player], board: GameBoard, clock: ChessClock):
        self.players = players
        self.board = board
        self.clock = clock

    def start(self):
        self.clock.start()

        # The main game loop executes here
        while self.game_running:
            self.board.draw()
            move = self.__retrieve_input()
            self.board.move_piece(move)
            self.clock.switch()
            self.turn_counter += 1

        self.clock.stop()

    def __retrieve_input(self) -> Move:  # __before the method labels it as private -> can only be used within class
        """ This function will receive input from the player, either human or machine """
        input("Give me something!")
