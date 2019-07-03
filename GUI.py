import ChessGameElements
import tkinter as tk
import PIL.Image
import PIL.ImageTk
from PIL import Image
import time

class GameBoard(tk.Frame):
    def __init__(self, parent, rows=8, columns=8, size=32, color1="white", color2="blue"):
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

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

    def addpiece(self, name, image, row=0, column=0):
        '''Add a piece to the playing board'''
        self.canvas.create_image(1, 1, image=image, tags=(name, "piece"), anchor="c")
        self.placepiece(name, row, column)

    def placepiece(self, name, row, column):
        '''Place a piece at the given row/column'''
        self.pieces[name] = (row, column)
        x0 = (column * self.size) + int(self.size / 2)
        y0 = (row * self.size) + int(self.size / 2)
        self.canvas.coords(name, x0, y0)

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
            self.placepiece(name, self.pieces[name][0], self.pieces[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")

    def get_size(self):
        return self.size


def generate_game_board():
    root = tk.Tk()
    board = GameBoard(root)
    piece_size = int(board.get_size() * 0.8)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)

    color = "B"
    kind = "P"
    image = PIL.Image.open("./icons/" + color + kind + ".PNG")
    image = image.resize((piece_size, piece_size), Image.ANTIALIAS)
    piece1 = PIL.ImageTk.PhotoImage(image)
    for rank in range(8):
        name = color + kind + str(rank)
        board.addpiece(name, piece1, 1, rank)

    kind = "R"
    image = PIL.Image.open("./icons/" + color + kind + ".PNG")
    image = image.resize((piece_size, piece_size), Image.ANTIALIAS)
    piece2 = PIL.ImageTk.PhotoImage(image)
    for rank in "07":
        name = color + kind + rank
        board.addpiece(name, piece2, 0, int(rank))

    kind = "N"
    image = PIL.Image.open("./icons/" + color + kind + ".PNG")
    image = image.resize((piece_size, piece_size), Image.ANTIALIAS)
    piece3 = PIL.ImageTk.PhotoImage(image)
    for rank in "16":
        name = color + kind + rank
        board.addpiece(name, piece3, 0, int(rank))

    kind = "B"
    image = PIL.Image.open("./icons/" + color + kind + ".PNG")
    image = image.resize((piece_size, piece_size), Image.ANTIALIAS)
    piece4 = PIL.ImageTk.PhotoImage(image)
    for rank in "25":
        name = color + kind + rank
        board.addpiece(name, piece4, 0, int(rank))

    kind = "Q"
    image = PIL.Image.open("./icons/" + color + kind + ".PNG")
    image = image.resize((piece_size, piece_size), Image.ANTIALIAS)
    piece5 = PIL.ImageTk.PhotoImage(image)
    rank = "3"
    name = color + kind + rank
    board.addpiece(name, piece5, 0, int(rank))

    kind = "K"
    image = PIL.Image.open("./icons/" + color + kind + ".PNG")
    image = image.resize((piece_size, piece_size), Image.ANTIALIAS)
    piece6 = PIL.ImageTk.PhotoImage(image)
    rank = "4"
    name = color + kind + rank
    board.addpiece(name, piece6, 0, int(rank))

    color = "W"
    kind = "P"
    image = PIL.Image.open("./icons/" + color + kind + ".PNG")
    image = image.resize((piece_size, piece_size), Image.ANTIALIAS)
    piece7 = PIL.ImageTk.PhotoImage(image)

    for rank in range(8):
        name = color + kind + str(rank)
        board.addpiece(name, piece7, 6, rank)

    kind = "R"
    image = PIL.Image.open("./icons/" + color + kind + ".PNG")
    image = image.resize((piece_size, piece_size), Image.ANTIALIAS)
    piece8 = PIL.ImageTk.PhotoImage(image)
    for rank in "07":
        name = color + kind + rank
        board.addpiece(name, piece8, 7, int(rank))

    kind = "N"
    image = PIL.Image.open("./icons/" + color + kind + ".PNG")
    image = image.resize((piece_size, piece_size), Image.ANTIALIAS)
    piece9 = PIL.ImageTk.PhotoImage(image)
    for rank in "16":
        name = color + kind + rank
        board.addpiece(name, piece9, 7, int(rank))

    kind = "B"
    image = PIL.Image.open("./icons/" + color + kind + ".PNG")
    image = image.resize((piece_size, piece_size), Image.ANTIALIAS)
    piece10 = PIL.ImageTk.PhotoImage(image)
    for rank in "25":
        name = color + kind + rank
        board.addpiece(name, piece10, 7, int(rank))

    kind = "Q"
    image = PIL.Image.open("./icons/" + color + kind + ".PNG")
    image = image.resize((piece_size, piece_size), Image.ANTIALIAS)
    piece11 = PIL.ImageTk.PhotoImage(image)
    rank = "3"
    name = color + kind + rank
    board.addpiece(name, piece11, 7, int(rank))

    kind = "K"
    image = PIL.Image.open("./icons/" + color + kind + ".PNG")
    image = image.resize((piece_size, piece_size), Image.ANTIALIAS)
    piece12 = PIL.ImageTk.PhotoImage(image)
    rank = "4"
    name = color + kind + rank
    board.addpiece(name, piece12, 7, int(rank))
    root.mainloop()


if __name__ == "__main__":
    generate_game_board()
