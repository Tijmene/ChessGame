from __future__ import annotations
from source.Board.GameBoard import GameBoard
from source.ChessUtils.Move import Move
from source.ChessUtils.Position import Position as Pos
from source.ChessUtils.Standing import Standing
import copy


class GameTree:
    def __init__(self, board: GameBoard, move: Move = None, depth_level: int = 0):
        self.board = board  # The state of the board in this node
        self.move = move    # The move that was made that led to this board state.
        self.parent = None
        self.children: dict = None
        self.depth_level = depth_level

    def create_future_state(self, move: Move):
        """ Is called on a node to add a child with the transformed Board after the input move """
        copy_board = copy.deepcopy(self.board)
        copy_board.move_piece(move)
        child = GameTree(board=copy_board, move=move, depth_level=self.depth_level + 1)
        self.__add_child(child)

    def __add_child(self, child: GameTree):
        if self.children is None:
            self.children = {}
        self.children[child.move.short_str()] = child
        child.parent = self

    def evaluate(self) -> int:
        return self.board.evaluate()

    def remove(self):
        """ Removes self from parents list of children """
        del self.parent.children[self.move.short_str()]
        del self.children
        del self.board
        del self.move

    def __get_root(self):
        """ Returns the root of the GameTree"""
        if self.parent is None:
            return self
        else:
            self.parent.get_root

    def get_all_leaves(self):
        # first find the root node:
        root = self.__get_root()
        first_order_nodes = root.children.values()
        for first_order_node in first_order_nodes:
            leaves = root.get_leaves()


    def evaluate(self) -> [(Move, Standing)]:
        """ Returns all moves that are possible directly from the root of the tree paired with their average standing"""


if __name__ == "__main__":
    testBoard1 = GameBoard()
    testBoard1.generate_default_setup()
    tree = GameTree(board=testBoard1)

    child1 = tree.create_future_state(Move(Pos('A', 2), Pos('A', 4)))
    child2 = child1.create_future_state(Move(Pos('A', 7), Pos('A', 6)))
    print(child1.board)
    print(child2.board)