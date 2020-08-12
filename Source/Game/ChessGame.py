from Source.Players.Player import Player
from Source.Board.GameBoard import GameBoard
from Source.Clocks.ChessClock import ChessClock
from Source.ChessUtils.Move import Move


class ChessGame:
    players: [Player]
    board: GameBoard
    clock: ChessClock
    gameRunning: bool = True

    def __init__(self, players: [Player], board: GameBoard, clock: ChessClock):
        self.players = players
        self.board = board
        self.clock = clock

    def start(self):
        self.clock.start()

        # The main game loop executes here
        while self.gameRunning:
            self.board.draw()
            move = self.__retrieve_input()
            self.board.move_piece(move)
            self.clock.switch()

        self.clock.stop()

    def __retrieve_input(self) -> Move:  # __before the method labels it as private -> can only be used within class
        """ This function will receive input from the player, either human or machine """
