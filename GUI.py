import ChessGameElements
import tkinter as tk
import PIL.Image
import PIL.ImageTk
from PIL import Image


class GameBoard(tk.Frame):
    def __init__(self, parent, state_board, rows=8, columns=8, size=32, color1="white", color2="blue"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.pieces = {}

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)
        self.setup(state_board)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

    def add_piece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(1, 1, image=image, tags=(name, "piece"), anchor="c")
        self.place_piece(name, row, column)

    def place_piece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size / 2)
        y0 = (row * self.size) + int(self.size / 2)
        self.canvas.coords(name, x0, y0)

    def update_board(self, state_board):
        for pos in state_board:
            piece = state_board[pos]
            if piece is not None:
                piece_name = piece.get_name()
                position = piece.get_position()
                vec_rank, vec_file = position.to_vec()
                self.pieces[piece_name] = (vec_rank, vec_file)

        for name in self.pieces:
            self.place_piece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width - 1) / self.columns)
        ysize = int((event.height - 1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
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
        for name in self.pieces:
            self.place_piece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def get_size(self):
        return self.size

    def setup(self, state_board):
        piece_size = int(self.get_size() * 0.8)
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
                position = piece.get_position()
                (vec_pos_f, vec_pos_r) = position.to_vec()
                self.add_piece(piece_name, globals()['chess_piece%s' % piece_name], vec_pos_f, vec_pos_r)
