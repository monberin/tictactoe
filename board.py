import random
import copy


class BSTNode(object):
    """Represents a node for a linked binary search tree."""

    def __init__(self, data, left=None, right=None):
        self.data = data
        self.left = left
        self.right = right


class LinkedBinaryTree:
    """
    represents a binary tree
    """

    def __init__(self, root):
        """
        initialises a tree
        """
        self.key = root
        self.left_child = None
        self.right_child = None

    def insert_left(self, new_node):
        """
        adds a left branch to a tree
        """
        if self.left_child == None:
            self.left_child = LinkedBinaryTree(new_node)
        else:
            t = LinkedBinaryTree(new_node)
            t.left_child = self.left_child
            self.left_child = t

    def insert_right(self, new_node):
        """
        adds a right branch to a tree
        """
        if self.right_child == None:
            self.right_child = LinkedBinaryTree(new_node)
        else:
            t = LinkedBinaryTree(new_node)
            t.right_child = self.right_child
            self.right_child = t

    def get_right_child(self):

        return self.right_child

    def get_left_child(self):
        return self.left_child

    def get_leaves(self):
        """
        returns a list with all leaves of a tree
        """
        leaves = []

        def rec_search(tree):
            if tree.left_child is None and tree.right_child is None:
                leaves.append(tree.key)
            else:
                if tree.left_child:
                    rec_search(tree.left_child)
                if tree.right_child:
                    rec_search(tree.right_child)
        rec_search(self)
        return leaves


class Board:
    """
    class to represent a tic tac toe board
    """

    def __init__(self):
        """
        initialises the board
        """
        self.state = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
        self.last_pos = 0
        self.last_symb = 'ox'

    def __str__(self):
        """
        returns a string representation of the board
        """
        return '\n'.join(['|'.join(el) for el in self.state])

    def check(self):
        """
        checks whether there is a winning combination on a board, returns a tuple with a bool and a winning symbol
        """
        for i in range(3):
            if self.state[i] == ['o', 'o', 'o'] or self.state[i] == ['x', 'x', 'x']:
                return (True, self.state[i][0])
            if self.state[0][i] == self.state[1][i] == self.state[2][i] and self.state[0][i] != ' ':
                return (True, self.state[0][i])
        if self.state[0][0] == self.state[1][1] == self.state[2][2] and self.state[0][0] != ' ':
            return (True, self.state[0][0])
        if self.state[0][2] == self.state[1][1] == self.state[2][0] and self.state[0][2] != ' ':
            return (True, self.state[0][2])

        l = 0
        for line in self.state:
            if ' ' not in line:
                l += 1
        if l != 3:
            return (False, 0)
        return (True, 'draw')

    def free_positions(self):
        """
        checks for free positions on the board
        """
        free = []
        for row in range(3):
            for col in range(3):
                if self.state[row][col] == ' ':
                    free.append((row, col))
        return free

    def add_position(self, row, col, item):
        """
        adds a position on a board
        """
        self.state[row][col] = item
        self.last_pos = (row, col)
        self.last_symb = item

    def make_move(self, item):
        """
        for user to make a move
        """
        row = int(input('row: '))
        col = int(input('col: '))
        if (row, col) in self.free_positions():
            self.add_position(row, col, item)
        else:
            raise NotValidMoveException
        print(self)

    def regenerate(self):
        """
        generating a board and a tree of choces for computer based on the current board position
        """
        tree = LinkedBinaryTree(self.state)

        def tree_rec(board, tree):
            if board.last_symb == 'x':
                symbol = 'o'
                self.last_symb == 'o'
            else:
                symbol = 'x'
                self.last_symb = 'x'

            free_moves = copy.deepcopy(board.free_positions())
            if len(free_moves) <= 1:
                branch = copy.deepcopy(board)
                branch.add_position(free_moves[0][0], free_moves[0][1], symbol)
                tree.insert_left(branch)
            else:
                move1 = random.choice(free_moves)
                free_moves.remove(move1)
                move2 = random.choice(free_moves)

                branch1 = copy.deepcopy(board)
                branch2 = copy.deepcopy(board)

                branch1.add_position(move1[0], move1[1], symbol)
                branch2.add_position(move2[0], move2[1], symbol)

                tree.insert_left(branch1)
                tree.insert_right(branch2)

                tree_rec(branch1, tree.get_left_child())
                tree_rec(branch2, tree.get_right_child())

        tree_rec(self, tree)
        branch1_points = self.points(tree.left_child.get_leaves())
        branch2_points = self.points(tree.right_child.get_leaves())
        if branch1_points > branch2_points:
            return tree.left_child.key
        return tree.right_child.key

    def computer_move(self):
        self.state = self.regenerate().state
        print(self)

    @staticmethod
    def points(state_list):
        """
        counts the winning points for computer
        """
        points = 0
        points += state_list.count('x')
        points -= state_list.count('o')
        return points


class NotValidMoveException(Exception):
    pass
