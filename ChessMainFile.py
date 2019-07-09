from Position import Position as Pos
from Game import Game
import tkinter as tk

if __name__ == "__main__":
    # setup the state of the game and the graphical representation of the board
    root = tk.Tk()
    game = Game(root)
    # Move a chess piece by giving the current position and the the desired position (Pawn from A2 to A4
    # game.move_piece(Pos('A', 2), Pos('A', 4), update_GUI=True)
    # At the moment updates the entire board by going over all pieces. Implementation to only changing something that
    # has changed is desirable.

    # Display the graphical representation of the board
    root.mainloop()
