from Source.Players.Player import Player
from Source.ChessUtils.Move import Move
from Source.ChessUtils.Position import Position as Pos
from Source.Learning.GameTree import GameTree
from Source.Board.GameBoard import GameBoard
import copy


class AIPlayer(Player):
    current_search_depth = 0
    max_search_depth = 6    # The depth of the search tree, a level is a round in which both players have taken a turn

    current_prune_depth = 0
    max_prune_depth = 3     # The depth at which the search tree should be pruned.

    current_search_breadth = 0
    max_search_breadth = 4  # The breadth of the search tree

    response_breadth = 1

    def get_next_move(self, board: GameBoard) -> Move:
        # Create a new game tree with the current state of the board
        board_without_gui = GameBoard(copy.deepcopy(board.square_mapping))
        game_tree = GameTree(board=board_without_gui)

        self.__expand_game_tree(game_tree)
        move = self.__evaluate_game_tree(game_tree)

    def __expand_game_tree(self, game_tree: GameTree):
        """ Calculates the future states for a given GameTree Node """

        # The maximum depth has been reached, don't calculate any more future states.
        if game_tree.depth_level >= self.max_search_depth:
            return
        else:
            interesting_moves = self.__generate_moves(game_tree.board)

            for interesting_move in interesting_moves:
                game_tree.create_future_state(interesting_move)

            if self.depth_level % self.current_prune_depth == 0:
                self.prune_game_tree(game_tree)

            # Recursively call the function on the children of the GameTree
            for game_node in game_tree.children.values():
                self.__expand_game_tree(game_node)

    def __generate_moves(self, board: GameBoard) -> [Move]:
        """ Generates possible moves from a given board. Interesting squares are determined and all the possible
         moves for each of these ssquares are generated. This list of moves is returned"""
        high_value_squares = self.__predict_high_value_squares(board=board)
        interesting_moves = []

        for high_value_square in high_value_squares:
            piece = board.query(high_value_square)
            legal_moves = piece.get_legal_moves(pos=high_value_square,
                                                square_mapping=board.square_mapping)

            for target_pos in legal_moves.possible_moves + legal_moves.possible_attacks:
                interesting_moves.append(Move(from_pos=high_value_square, to_pos=target_pos))

        return interesting_moves

    def __predict_high_value_squares(self, board: GameBoard) -> [Pos]:
        """ Function that uses a DNN to evaluate the GameTree Node and returns a list of high value squares"""
        high_value_squares = []
        # Generate list of high value squares with probability that the piece to be move is going to be in that square
        # Take the first self.search_breadth elements from this list and return these.
        return high_value_squares

    def __prune_future_states(self, game_tree: GameTree):
        """ Prunes the GameTree by removing branches that have low evaluations """
        for leaf in game_tree.get_all_leaves():
            self.evaluate_future_state(leaf.board)

    def __evaluate_game_tree(self, game_tree: GameTree) -> Move:
        """ Calculate the point difference between this player and the opponent in this future state """
        return None





