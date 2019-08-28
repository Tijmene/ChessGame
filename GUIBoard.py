import tkinter as tk
import PIL.Image
import PIL.ImageTk
from PIL import Image
from Position import vec_to_pos

class GUIBoard(tk.Frame):
    def __init__(self, parent, state_board, turn_counter, rows=8, columns=8, size=32, piece_scale=0.7, hit_scale=0.1,
                 color_white="white", color_black="gray63", color_selected_square="gold",
                 color_target_hit="orange red", color_target_square="khaki1"):
        self.rows = rows                    # Amount of rows that the board has
        self.columns = columns              # Amount of columns that the board has
        self.size = size                    # Size of a square in pixels
        self.color1 = color_white           # Color of the "White" tiles
        self.color2 = color_black           # Color of the "Black tiles
        self.color3 = color_selected_square # Color of the tile that is selected
        self.color4 = color_target_hit      # Color of the target square
        self.color5 = color_target_square   # Color of the target square if it has a enemy piece on it
        self.pieces = {}                    # Dictionary that will contain the name of the pieces with their location
        self.selected_square = None         # Position of the Square that is currently selected
        self.piece_size = int(self.size * piece_scale)    # Size of the pieces on the chessboard
        self.hit_scale = hit_scale          # Scale the hit circle
        self.state_board = state_board      # State of the board
        self.turn_counter = turn_counter    # Turn counter that keeps track of the turns
        self.piece_to_move = None           # Variable that stores a piece to potentially move it with the next click

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        self.setup_gui(state_board.get_game_state())

        # this binding will cause a refresh if the user interactively changes the window size
        self.canvas.bind("<Configure>", self.refresh)
        # this binding will interact with the chessboard via left mouse-clicks.
        self.canvas.bind("<Button-1>", self.interact_mouse)

    def add_piece(self, name, image, pos):
        """Add a piece to the playing board"""
        self.canvas.create_image(1, 1, image=image, tags=(name, "piece"), anchor="c")
        self.place_piece(name, pos)

    def place_piece(self, name, pos):
        """Place a piece at the given row/column"""
        self.pieces[name] = pos
        vec_x, vec_y = pos.to_vec()
        x0 = (vec_x * self.size) + int(self.size / 2)
        y0 = (vec_y * self.size) + int(self.size / 2)
        self.canvas.coords(name, x0, y0)

    def remove_piece(self, name):
        self.canvas.delete(name)

    def update_board(self, state_board):
        """This function can be used if the user wants to see a snapshot of the board but runs the game mainly on the
        state_board without showing the GUI"""
        self.turn_counter += 1
        for pos in state_board:
            piece = state_board[pos]
            if piece is not None:
                piece_name = piece.get_name()
                position = piece.get_position()
                self.pieces[piece_name] = position

        for name in self.pieces:
            self.place_piece(name, self.pieces[name])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def interact_mouse(self, event):
        """A square is highlighted if: It has a piece on it AND it is the turn of the players the piece belongs to.
        The piece on the highlighted square will be moved if a valid target position is selected with the next click"""
        vec_x = event.x//self.size
        vec_y = event.y//self.size
        x1 = (vec_x * self.size)
        y1 = (vec_y * self.size)
        x2 = x1 + self.size
        y2 = y1 + self.size

        new_pos = vec_to_pos(vec_x, vec_y)
        selected_piece = self.state_board.query_game_board(new_pos)
        turn_bool = False

        if selected_piece is not None:
            even_turn = self.turn_counter % 2 == 0
            turn_bool = (selected_piece.get_color() == "W" and even_turn) or (
                    selected_piece.get_color() == "B" and not even_turn)

        if turn_bool:
            # Highlight the square of the currently selected piece
            self.piece_to_move = selected_piece
            self.canvas.delete("square_selected")
            self.canvas.delete("square_target")
            self.selected_square = new_pos
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=self.color3, tags="square_selected")
            # Highlight the possible target squares for the currently selected piece
            legal_moves = self.state_board.get_legal_moves(new_pos)
            for move in legal_moves:
                row, col = move.to_vec()
                x1 = (row * self.size) + self.size * self.hit_scale
                y1 = (col * self.size) + self.size * self.hit_scale
                x2 = x1 + self.size - self.size * (2 * self.hit_scale)
                y2 = y1 + self.size - self.size * (2 * self.hit_scale)
                if self.state_board.query_game_board(move) is not None:
                    self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill=self.color4, tags="square_target")
                else:
                    self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill=self.color5, tags="square_target")

            self.canvas.tag_raise("piece")

        prev_pos = self.selected_square
        if not turn_bool and prev_pos is not None and self.state_board.check_move(prev_pos, new_pos):
            target_piece = self.state_board.query_game_board(new_pos)
            if target_piece is not None and new_pos.to_string() != prev_pos.to_string():
                self.canvas.delete(target_piece.get_name())
            self.state_board.move_piece_state(self.selected_square, new_pos)
            piece_name = self.piece_to_move.get_name()
            self.place_piece(piece_name, new_pos)
            self.piece_to_move = None
            self.canvas.delete("square_selected")
            self.canvas.delete("square_target")
            self.turn_counter += 1
            self.selected_square = None

    def refresh(self, event):
        """Redraw the board, possibly in response to window being resized"""
        x_size = int((event.width - 1) / self.columns)
        y_size = int((event.height - 1) / self.rows)
        self.size = min(x_size, y_size)
        self.canvas.delete("square")
        self.canvas.delete("square_selected")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2

        # Redraw the square that is currently selected
        selected_square = self.selected_square
        if selected_square is not None:
            vec_x, vec_y = selected_square.to_vec()
            x1 = (vec_x * self.size)
            y1 = (vec_y * self.size)
            x2 = x1 + self.size
            y2 = y1 + self.size
            color = self.color3
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square_selected")

        # Redraw all the pieces that are on the board
        for name in self.pieces:
            self.place_piece(name, self.pieces[name])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square_selected")
        self.canvas.tag_lower("square")

    def setup_gui(self, state_board):
        """Creates the GUI and sets the pieces up as they are listed in the state_board"""
        piece_size = self.piece_size
        self.pack(side="top", fill="both", expand="true", padx=4, pady=4)
        for pos in state_board:
            piece = state_board[pos]
            if piece is not None:
                image_name = piece.color + piece.kind
                image_file = PIL.Image.open("./icons/" + image_name + ".PNG")
                image_file = image_file.resize((piece_size, piece_size), Image.ANTIALIAS)

                # A new variable has to be created for every piece
                piece_name = piece.get_name()
                globals()['chess_piece%s' % piece_name] = PIL.ImageTk.PhotoImage(image_file)
                pos = piece.get_position()
                self.add_piece(piece_name, globals()['chess_piece%s' % piece_name], pos)
