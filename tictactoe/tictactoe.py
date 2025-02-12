"""
Tic Tac Toe Player
"""

import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY], [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    empty = 0
    x = 0
    o = 0
    if terminal(board) == True:
        return EMPTY
    for i in board:
        for j in i:
            if j == EMPTY:
                empty += 1
            elif j == X:
                x += 1
            elif j == O:
                o += 1
    if empty == 9:
        return X
    elif x == o:
        return X
    elif x > o:
        return O
    raise NotImplementedError(f"player Function empty: {empty} X: {x} O: {o}")


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == EMPTY:
                actions.add((i, j))
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row, cell = action

    if board[row][cell] != EMPTY:
        raise IndexError(f"Place already has been used by {results[row][cell]}")

    results = copy.deepcopy(board)
    P_move = player(results)
    results[row][cell] = P_move
    return results


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    sym = X  # First Checking for X
    for _ in range(2):
        # Checking Horizontal Winning
        for i in board:
            w = 0  # wining count
            for j in i:
                if j == sym:
                    w += 1
            if w == 3:
                return sym
        # Checking Vertical Winning
        for i in range(3):
            w = 0
            for j in board:
                if j[i] == sym:
                    w += 1
            if w == 3:
                return sym
        # Checking diagonally Winning
        w = 0
        for i in range(3):
            if board[i][i] == sym:
                w += 1
        if w == 3:  # Its a Backslash of sym
            return sym
        if board[0][2] == board[1][1] == board[2][0] == sym:
            return sym
        sym = O  # Now check for O
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) is not None or (not any(EMPTY in sublist for sublist in board)):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if terminal(board):
        win = winner(board)
        if win == X:
            return 1
        elif win == O:
            return -1
        else:
            return 0


def minimax(board):
    """Returns the optimal action for the current player on the board."""
    if terminal(board):
        return None  # No action needed if the game is over

    if player(board) == X:
        best_action, best_value = max_value(board)
        return best_action
    else:
        best_action, best_value = min_value(board)
        return best_action  # Return the action, not the value


def min_value(board):
    if terminal(board):
        return None, utility(board)  # Return None for action, utility for value

    v = math.inf
    best_action = None
    for action in actions(board):
        _, value = max_value(
            result(board, action)
        )  # Discard the action returned by max_value
        if value < v:
            v = value
            best_action = action
            if v == -1:
                return best_action, v
    return best_action, v


def max_value(board):
    if terminal(board):
        return None, utility(board)  # Return None for action, utility for value

    v = -math.inf
    best_action = None
    for action in actions(board):
        _, value = min_value(
            result(board, action)
        )  # Discard the action returned by min_value
        if value > v:
            v = value
            best_action = action
            if v == 1:
                return best_action, v
    return best_action, v
