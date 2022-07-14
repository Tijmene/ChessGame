from source.Board.GameBoard import GameBoard
from source.ChessUtils.Color import Color
from source.ChessUtils.Move import Move
from source.ChessUtils.Position import Position as Pos, vec_to_pos
from source.ChessUtils.PossibleMoveSet import PossibleMoveSet
from source.ChessUtils.MoveGenerator import generate_moves
from source.Players import HumanPlayer

import tkinter as tk
import PIL.Image
import PIL.ImageTk
from PIL import Image


class GUIBoard(tk.Frame):
    """
    Creates the graphical user interface (GUI) that displays the current state of the :class:`GameBoard`.
    :class:`Player`s use this GUI to select their next :class:`Move`.
     """
    game_board: GameBoard
    connections: dict
    previous_possible_moves: PossibleMoveSet

    def __init__(self, game_board: GameBoard, **graphical_options):
        self.game_board = game_board
        self.connections = {}

        # Fields related to the display of the board and their Default values
        self.rows = 8                           # Amount of rows that the board has
        self.columns = 8                        # Amount of columns that the board has
        self.size = 32                          # Size of a square in pixels
        self.color_white = "white"              # Color of the "White" tiles
        self.color_black = "gray63"             # Color of the "Black tiles
        self.color_selected_square = "gold"     # Color of the tile that is selected
        self.color_target_hit = "orange red"    # Color of the target square if it has an enemy piece on it
        self.color_target_square = "khaki1"     # Color of the target square if it has no enemy in it
        self.piece_size = int(self.size * 0.7)  # Size of the pieces on the chessboard
        self.hit_scale = 0.05                   # Scale the hit circle
        self.is_opened = True                   # Used to help kill the application

        #  Default values are overridden by provided values if they are present in the graphical_options variable.
        for (option, value) in graphical_options.items():
            setattr(self, option, value)

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
        self.canvas.bind("<Configure>", self.__handle_refresh)                 # Reconfigurations such as a resize
        self.canvas.bind("<Button-1>", self.__handle_mouse_click)              # Left mouse clicks
        self.tk_root.protocol('WM_DELETE_WINDOW', self.__handle_window_close)  # Handle window close
        # self.canvas.bind("WM_DELETE_WINDOW", self.__handle_window_close)     # Handle window close

        # Initiate the latest move set with an empty move set
        self.previous_possible_moves = PossibleMoveSet()

    def connect_player(self, player: HumanPlayer) -> None:
        """
        Connects a :class:`HumanPlayer`to the GUI so that it can interact with it.
        :param player: the :class:`Player` that has to be connected to the GUI.
        """
        self.connections[player.color] = player.gui_connection

    def update(self) -> None:
        """
        Update the GUI, this method is called repeatedly from the main game loop to refresh the gui each game step.
        """
        self.tk_root.update_idletasks()
        self.tk_root.update()

    def state_update(self, new_board: GameBoard) -> None:
        """
        Update the state of the GUI with the new :class:`GameBoard` such that on the next update the GUI shows the
        updated state of the board.
        :param new_board: The new :class:`GameBoard` that contains the latest state of the game.
        """
        self.game_board = new_board
        self.__remove_highlights()
        self.__place_pieces()

    def __handle_mouse_click(self, event):
        """ The GUI identifies the selected square and sends it to the ChessGame """
        vec_x = event.x // self.size
        vec_y = event.y // self.size
        pos_clicked_square = vec_to_pos(vec_x, vec_y)

        if pos_clicked_square in self.previous_possible_moves:
            self.send_selected_move(Move(from_pos=self.previous_possible_moves.from_position,
                                         to_pos=pos_clicked_square))
            self.__remove_highlights()
            self.previous_possible_moves = PossibleMoveSet()
        else:
            possible_moves = generate_moves(self.game_board, pos_clicked_square)
            self._highlight_squares(possible_moves)
            self.previous_possible_moves = possible_moves

    def send_selected_move(self, move: Move) -> None:
        """
        Sends the :class:`Move` generated by interaction with the GUI to the respective :class:`Player` who was
        interacting with the GUI.
        :param move: The :class:`Move` that has to be executed.
        """
        colors_turn = Color.WHITE if self.game_board.turn_counter % 2 == 1 else Color.BLACK
        self.connections[colors_turn].put(move)

    def _highlight_squares(self, possible_moves: PossibleMoveSet = PossibleMoveSet()) -> None:
        """
        highlights the squares for selected square, possible moves, and possible attacks on the board with their
        respective colors. If no argument is provided an empty move set is used which clears the highlights.
        :param possible_moves: the move set that has to be highlighted.
        :return:
        """
        self.__remove_highlights()

        if possible_moves.is_empty():
            return

        # A square is selected and has to be highlighted.
        self.canvas.itemconfigure(possible_moves.from_position.__str__() + "SQUARE", fill=self.color_selected_square)

        # Mark possible moves with circles on the GUI
        for move in possible_moves.possible_moves:
            self.__create_move_circle(move, self.color_target_square)

        # Mark possible attacks with circles on the GUI
        for attack in possible_moves.possible_attacks:
            self.__create_move_circle(attack, self.color_target_hit)

        # Raise the pieces so that they are position above circles, if they are present.
        self.canvas.tag_raise("piece")

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

    def __handle_window_close(self):
        print("The Chess application has been closed.")  # TODO: cause the game run loop to halt on closing via the gui
        self.is_opened = False
        self.tk_root.destroy()

    def __create_move_circle(self, pos: Pos, color: str):
        vec_x, vec_y = pos.to_vec()
        x1 = (vec_x * self.size) + self.size * self.hit_scale
        y1 = (vec_y * self.size) + self.size * self.hit_scale
        x2 = x1 + self.size - self.size * (2 * self.hit_scale)
        y2 = y1 + self.size - self.size * (2 * self.hit_scale)
        self.canvas.create_oval(x1, y1, x2, y2, outline="black", fill=color, tags="square_target")

    def __remove_highlights(self):
        if self.previous_possible_moves.is_not_empty():
            self.__restore_default_color(self.previous_possible_moves.from_position)
        self.canvas.delete("square_target")

    def __restore_default_color(self, position: Pos):
        tag = position.__str__()
        even_file = ord(tag[0]) % 2 == 0
        even_rank = int(tag[1]) % 2 == 0

        if even_file and even_rank or not even_file and not even_rank:
            color = self.color_black
        else:
            color = self.color_white
        self.canvas.itemconfigure(tag + "SQUARE", fill=color)

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
        for pos_str, piece in self.game_board.square_mapping.items():
            if piece is not None:
                pos = Pos(pos_str[0], int(pos_str[1]))
                vec_x, vec_y = pos.to_vec()
                x0 = (vec_x * self.size) + int(self.size / 2)
                y0 = (vec_y * self.size) + int(self.size / 2)
                self.canvas.coords(piece.identifier, x0, y0)

    def __load_pieces(self):
        for pos, piece in self.game_board.square_mapping.items():
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
        if self.previous_possible_moves.is_not_empty():
            vec_x, vec_y = self.previous_possible_moves.from_position.to_vec()
            x1 = (vec_x * self.size)
            y1 = (vec_y * self.size)
            x2 = x1 + self.size
            y2 = y1 + self.size
            self.canvas.create_rectangle(x1, y1, x2, y2, outline="black",
                                         fill=self.color_selected_square, tags="square_selected")
