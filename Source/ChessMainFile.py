from Position import Position as Pos
from Game import Game, construct_possible_state_tree
import tkinter as tk
import timeit
# from ML import create_ml_input

if __name__ == "__main__":
    # setup the state of the game and the graphical representation of the board
    root = tk.Tk()
    game = Game(root)
    # Move a chess piece by giving the current position and the the desired position (Pawn from A2 to A4
    # game.move_piece(Pos('A', 2), Pos('A', 4), update_GUI=True)
    # game.move_piece(Pos('A', 7), Pos('A', 6), update_GUI=True)

    # At the moment updates the entire board by going over all pieces. Implementation to only changing something that
    # has changed is desirable.

    state = game.get_game_state()
    start = timeit.default_timer()
    turn_counter = game.get_turn_counter()
    possible_future_states = construct_possible_state_tree(2, state, turn_counter)
    stop = timeit.default_timer()
    print('Time for possible worlds: ', stop - start)

    # start = timeit.default_timer()
    # ml_input = create_ml_input(state)
    # stop = timeit.default_timer()
    # print('Time for ML input: ', stop - start)
    # Display the graphical representation of the board
    root.mainloop()

