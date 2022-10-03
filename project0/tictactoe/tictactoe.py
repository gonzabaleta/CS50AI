"""
Tic Tac Toe Player
"""

import math
from copy import deepcopy

X = "X"
O = "O"
EMPTY = None
SIZE = 3


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    x_count = 0
    o_count = 0

    for row in board:
        for cell in row:
            if cell == X:
                x_count += 1
            elif cell == O:
                o_count += 1
    
    if not x_count and not o_count:
        return X # If board is empty, then it's X's turn 
    elif x_count == o_count:
        return X # If the amount of X's equals the amount of O's, then it's X's turn.
    elif o_count < x_count:
        return O # if the amount of X's is greater than the amount of O's, then it's O's turn
    else:
        return None


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    actions = set()

    for i, row in enumerate(board): 
        for j, cell in enumerate(row):
            if cell == EMPTY:
                actions.add((i, j))
    
    return actions


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Check if the action is a tuple of two numbers between 0 and 2
    for cell in action:
        if cell not in [0, 1, 2]:
            raise ValueError("Invalid action type")

    symbol = player(board) 
    copy = deepcopy(board) # create a deep copy of the list so that the original is not affected

    row = action[0]
    col = action[1]

    # check that the cell is not already in use
    if (copy[row][col] is not EMPTY):
        raise ValueError("Invalid action: cell already in use")

    # fill the cell with the player's symbol
    copy[row][col] = symbol

    return copy


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    # check for winner in rows
    for row in board:
        symbol = row[0]

        is_winner = True
        for cell in row:
            if cell != symbol:
                is_winner = False
        
        if (is_winner):
            return symbol

    # check for winner in cols
    for j in range(SIZE):
        symbol = board[0][j]

        is_winner = True
        for i in range(SIZE):
            if board[i][j] != symbol:
                is_winner = False
        
        if (is_winner):
            return symbol

    # check for winner in diagonals
    ### From top-left:
    symbol = board[0][0]
    if (board[1][1] == symbol and board[2][2] == symbol):
        return symbol
    
    ### From top-right
    symbol = board[0][2]
    if(board[1][1] == symbol and board[2][0] == symbol):
        return symbol

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If there is a winner, then it's over
    if (winner(board)):
        return True

    # if there are empty cells, it's not over
    for row in board:
        for cell in row:
            if cell == EMPTY:
                return False
    
    # if no empty cells, then it's over
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win_player = winner(board)

    if win_player == X:
        return 1
    elif win_player == O:
        return -1
    else:
        return 0

    raise NotImplementedError


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # If terminal board, then no action to take
    if terminal(board):
        return None

    # initialize variables
    player_type = 'max' if player(board) == X else 'min' # define the type of player (min or max)
    best_action = None # keep track of the best action to take while we consider
    possible_actions = actions(board)

    # If it's max player, then try to maximize the actions taken by the min player
    if (player_type == 'max'):
        # keep track of the highest action score (start with the lowest number)
        highest = -1

        # consider each action
        for action in possible_actions:
            # consider what the min player would do
            v = min_value(result(board, action))

            # if the resulting value is higher than the current, then it's the best action so far
            if v > highest:
                best_action = action
                highest = v

    # if it's min player, try to minimize the actions taken by the max player
    elif (player_type == 'min'):
        # keep track of the lowest action score (start with the highest number)
        lowest = 1

        # consider each action
        for action in possible_actions:
            # consider what the max player would do
            v = max_value(result(board, action))

            # if the resulting value is lower than the current, then it's the best action so far
            if v < lowest:
                best_action = action
                lowest = v
                
    return best_action


def max_value(board):
    if terminal(board):
        return utility(board)
    
    highest = -1
    for action in actions(board):
        highest = max(highest, min_value(result(board, action)))
    
    return highest

def min_value(board):
    if terminal(board):
        return utility(board)

    lowest = 1
    for action in actions(board):
        lowest = min(lowest, max_value(result(board, action)))

    return lowest
    
