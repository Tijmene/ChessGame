from Source.ChessUtils.Position import Position as Pos, vec_to_pos
from Source.ChessUtils.GUIResponse import GUIResponse
import tkinter as tk
import PIL.Image
import PIL.ImageTk
from PIL import Image


class GUIBoard(tk.Frame):
    """ Creates the graphical user interface (GUI) that displays the current state of the board """
    square_mapping: dict
    queue = None

    def __init__(self, square_mapping: dict, **graphical_options):
        self.square_mapping = square_mapping

        # Fields related to the display of the board and their Default values
        self.rows = 8                           # Amount of rows that the board has
        self.columns = 8                        # Amount of columns that the board has
        self.size = 32                          # Size of a square in pixels
        self.color_white = "white"              # Color of the "White" tiles
        self.color_black = "gray63"             # Color of the "Black tiles
        self.color_selected_square = "gold"     # Color of the tile that is selected
        self.color_target_hit = "orange red"    # Color of the target square
        self.color_target_square = "khakil"     # Color of the target square if it has a enemy piece on it
        self.piece_size = int(self.size * 0.7)  # Size of the pieces on the chessboard
        self.hit_scale = 0.1                    # Scale the hit circle

        #  Default values are overridden by provided values if they are present in the graphical_options variable.
        for (option, value) in graphical_options.items():
            setattr(self, option, value)

        self.highlighted_tag = None  # Location of the square currently highlighted
        self.selected_square = None  # Position of the Square that is currently selected
        self.piece_to_move = None    # Variable that stores a piece to potentially move it with the next click

        # Create the canvas on which everything is drawn.
        self.tk_root = tk.Tk()
        tk.Frame.__init__(self, self.tk_root)
        canvas_width = self.columns * self.size
        canvas_height = self.rows * self.size
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # Draw all elements in the canvas.
        self.__draw()

        # Bind actions to functions
        self.canvas.bind("<Configure>", self.__handle_refresh)        # Reconfigurations such as a resize
        self.canvas.bind("<Button-1>", self.__handle_mouse_click)  # Left mouse clicks
        # TODO: Handle closing of window event.

    def connect(self, queue):
        self.queue = queue

    def __handle_refresh(self, event):
        """ Redraw the board, possibly in response to window being resized """
        x_size = int((event.width - 1) / self.columns)
        y_size = int((event.height - 1) / self.rows)
        self.size = min(x_size, y_size)

        self.canvas.delete("square")
        self.__draw_checkerboard()

        self.canvas.delete("square_selected")
        self.__draw_selected_square()

        self.__place_pieces()

        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square_selected")
        self.canvas.tag_lower("square")

    def __handle_mouse_click(self, event):
        """ The GUI identifies the selected square and sends it to the ChessGame """
        vec_x = event.x // self.size
        vec_y = event.y // self.size

        pos_clicked_square = vec_to_pos(vec_x, vec_y)
        self.queue.put(pos_clicked_square)

    def update(self):
        """ This method can be called from outside of this class (e.g. from the main game loop) This updates the
        GUI. """
        message = self.__receive_messages()
        if message is not None:
            self.__handle_message(message)
        self.tk_root.update_idletasks()
        self.tk_root.update()

    def __receive_messages(self):
        """ Retrieves messages from the Queue and returns them if they are present, otherwise returns None """
        if self.queue.empty():
            return None
        else:
            return self.queue.get()

    def __handle_message(self, message: GUIResponse):
        self.__remove_highlights()

        if message.has_highlight():
            self.highlighted_tag = message.highlight.__str__()
            self.canvas.itemconfigure(self.highlighted_tag + "SQUARE", fill=self.color_selected_square)

    def __remove_highlights(self):
        if self.highlighted_tag:
            self.__restore_default_color(self.highlighted_tag)

    def __restore_default_color(self, tag: str):
        even_file = ord(tag[0]) % 2 == 0
        even_rank = int(tag[1]) % 2 == 0

        if even_file and even_rank or not even_file and not even_rank:
            color = self.color_black
        else:
            color = self.color_white
        self.canvas.itemconfigure(self.highlighted_tag + "SQUARE", fill=color)

    def __draw(self):
        self.pack(side="top", fill="both", expand="true", padx=4, pady=4)
        self.__draw_checkerboard()
        self.__load_pieces()
        self.__place_pieces()

    def __draw_checkerboard(self):
        color = self.color_black
        for row in range(self.rows):
            color = self.color_white if color == self.color_black else self.color_black
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                square_tag = "{file}{rank}SQUARE".format(file=chr(col + 65), rank=self.rows-row)
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags=("square", square_tag))
                color = self.color_white if color == self.color_black else self.color_black

    def __place_pieces(self):
        for pos_str, piece in self.square_mapping.items():
            if piece is not None:
                pos = Pos(pos_str[0], int(pos_str[1]))
                vec_x, vec_y = pos.to_vec()
                x0 = (vec_x * self.size) + int(self.size / 2)
                y0 = (vec_y * self.size) + int(self.size / 2)
                self.canvas.coords(piece.identifier, x0, y0)

    def __load_pieces(self):
        for pos, piece in self.square_mapping.items():
            if piece is not None:
                image_name = str(piece.color)[0] + piece.get_letter_code()
                image_file = PIL.Image \
                    .open("../icons/" + image_name + ".PNG") \
                    .resize((self.piece_size, self.piece_size), Image.ANTIALIAS)

                # Store every image in an unique global variable
                globals()['chess_piece%s' % piece.identifier] = PIL.ImageTk.PhotoImage(image_file)

                self.canvas.create_image(1, 1, image=globals()['chess_piece%s' % piece.identifier],
                                         tags=(piece.identifier, "piece"), anchor="c")

    def __draw_selected_square(self):
        # Redraw the square that is currently selected
        if self.selected_square is not None:
            vec_x, vec_y = self.selected_square.to_vec()
            x1 = (vec_x * self.size)
            y1 = (vec_y * self.size)
            x2 = x1 + self.size
            y2 = y1 + self.size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black",
                                         fill=self.color_selected_square, tags="square_selected")
