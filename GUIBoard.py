import tkinter as tk
import PIL.Image
import PIL.ImageTk
from PIL import Image
from Position import Position
from Position import vec_to_pos


class GUIBoard(tk.Frame):
    def __init__(self, parent, state_board, rows=8, columns=8, size=32, piece_scale=0.7, color1="white", color2="blue",
                 color3="yellow"):
        """size is the size of a square, in pixels"""

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.pieces = {}
        self.selected_square = None
        self.piece_size = int(self.get_size() * piece_scale)

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        self.setup_gui(state_board.get_game_state())

        # this binding will cause a refresh if the user interactively changes the window size
        self.canvas.bind("<Configure>", self.refresh)
        # this binding highlights the square that is clicked
        self.canvas.bind("<Button-1>", self.select_square)

    def add_piece(self, name, image, pos):
        """Add a piece to the playing board"""
        self.canvas.create_image(1, 1, image=image, tags=(name, "piece"), anchor="c")
        self.place_piece(name, pos)

    def place_piece(self, name, pos):
        """Place a piece at the given row/column"""
        self.pieces[name] = pos
        row, col = pos.to_vec()
        y0 = (row * self.size) + int(self.size / 2)
        x0 = (col * self.size) + int(self.size / 2)
        self.canvas.coords(name, x0, y0)

    def update_board(self, state_board):
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

    def select_square(self, event):
        row = event.y//self.size
        col = event.x//self.size
        x1 = (col * self.size)
        y1 = (row * self.size)
        x2 = x1 + self.size
        y2 = y1 + self.size

        # Only select the square if it has a piece on it
        pos = vec_to_pos(row, col)
        pos_list = [v.to_string() for v in self.pieces.values()]
        if pos.to_string() in pos_list:
            self.canvas.delete("square_selected")
            self.selected_square = vec_to_pos(row, col)
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=self.color3, tags="square_selected")
            self.canvas.tag_raise("piece")

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

        """Redraw the square that is currently selected"""
        selected_square = self.selected_square
        if selected_square is not None:
            row, col = selected_square.to_vec()
            x1 = (col * self.size)
            y1 = (row * self.size)
            x2 = x1 + self.size
            y2 = y1 + self.size
            color = self.color3
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square_selected")

        """Redraw all the pieces that are on the board"""
        for name in self.pieces:
            self.place_piece(name, self.pieces[name])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square_selected")
        self.canvas.tag_lower("square")

    def get_size(self):
        return self.size

    def setup_gui(self, state_board):
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
