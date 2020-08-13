from Source.Players.Player import Player
from Source.Board.GameBoard import GameBoard
from Source.Clocks.ChessClock import ChessClock
from Source.ChessUtils.Move import Move
import tkinter as tk


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

    def run(self):
        self.clock.start()
        received_move = None

        # The main game loop executes here
        while self.game_running:
            self.board.draw()
            if received_move is not None:
                self.board.move_piece(received_move)
                self.clock.switch()
                self.turn_counter += 1
                received_move = None

        self.clock.stop()
