from Source.Players.Player import Player
from Source.ChessUtils.Move import Move
from Source.ChessUtils.Position import Position as Pos
from Source.Learning.SearchTree import GameTree
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

    def calculate_next_move(self, board: GameBoard) -> Move:
        # Create a new game tree with the current state of the board
        board_without_gui = GameBoard(copy.deepcopy(board.square_mapping))
        game_tree = GameTree(board=board_without_gui)

        self.calculate_future_states(game_tree)
        move = self.evaluate_future_state(game_tree)

    def calculate_future_states(self, game_tree: GameTree):
        """ Calculates the future states for a given GameTree Node """

        # The maximum depth has been reached, don't calculate any more future states.
        if game_tree.depth_level >= self.max_search_depth:
            return
        else:
            high_value_squares = self.calculate_high_value_squares(game_tree)
            for high_value_square in high_value_squares:
                piece = game_tree.board.query(high_value_square)
                legal_moves = piece.get_legal_moves(pos=high_value_square,
                                                    square_mapping=game_tree.board.square_mapping)

                for move in legal_moves.possible_moves:
                    game_tree.create_future_state(Move(from_pos=high_value_square, to_pos=move))
                for move in legal_moves.possible_attacks:
                    game_tree.create_future_state(Move(from_pos=high_value_square, to_pos=move))

            # Simulate the response of the opponent
            for child in game_tree.children.values():
                response_move = self.simulate_response(child.board)
                child.create_future_state(response_move)

            if self.depth_level // 2 % self.current_prune_depth == 0:  # TODO: Divide by 2?
                self.prune_game_tree(game_tree)

            # Recursively call the function on the children of the GameTree
            for game in game_tree.get_all_leaves():
                self.calculate_future_states(game)

    def calculate_high_value_squares(self, board: GameBoard) -> [Pos]:
        """ Function that uses a DNN to evaluate the GameTree Node and returns a list of high value squares"""
        high_value_squares = []
        # Generate list of high value squares with probability that the piece to be move is going to be in that square
        # Take the first self.search_breadth elements from this list and return these.
        return high_value_squares

    def simulate_response(self, board: GameBoard) -> Move:
        """ Simulates the response for the opponent """
        # take only the n most likely responses where n = self.response_breadth
        return None

    def prune_future_states(self, game_tree: GameTree):
        """ Prunes the GameTree by removing branches that have low evaluations """
        for leaf in game_tree.get_all_leaves():
            self.evaluate_future_state(leaf.board)

    def evaluate_future_state(self, game_tree: GameTree) -> Move:
        """ Calculate the point difference between this player and the opponent in this future state """
        return None





