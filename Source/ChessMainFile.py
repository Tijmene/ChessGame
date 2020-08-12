from Source.ChessGame import ChessGame, construct_possible_state_tree
import tkinter as tk
import timeit
# from ML import create_ml_input

if __name__ == "__main__":
    # setup the state of the game and the graphical representation of the board
    root = tk.Tk()
    game = ChessGame(root)
    # Move a chess piece by giving the current position and the the desired position (Pawn from A2 to A4
    game.move_piece(Pos('A', 2), Pos('A', 4), update_GUI=True)
    game.move_piece(Pos('A', 7), Pos('A', 6), update_GUI=True)

    root.mainloop()

