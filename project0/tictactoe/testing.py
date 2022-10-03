from tictactoe import initial_state, player, actions, result, winner, terminal, utility, X, O, EMPTY

"""
    PLAYER 
"""
print("----- PLAYER -----")
# 1 -- returns X for initial state ✅
print("1 --", player(initial_state()))

# 2 -- returns X when x_count == o_count ✅
print("2 --", player([[X, O, EMPTY],
                      [EMPTY, EMPTY, EMPTY],
                      [EMPTY, EMPTY, EMPTY]]))

# 3 -- returns O when x_count > o_count ✅
print("3 --", player([[X, O, X],
                              [O, X, EMPTY],
                              [EMPTY, EMPTY, EMPTY]]))
print('\n')


"""
    ACTIONS
"""
print("----- ACTIONS -----")

# 1 -- returns all 9 actions for empty board ✅
print("1 --", actions(initial_state()))

# 2 -- returns returns (2, 1) for the following board: ✅
print("2 --", actions([[X, O, X],
                       [O, X, O],
                       [X, EMPTY, X]]))

# 2 -- returns returns {(0, 2), (1, 0), (1, 1), (2, 0), (2, 2)} for the following board: ✅
print("3 --", actions([[X, O, EMPTY],
                       [EMPTY, EMPTY, O],
                       [EMPTY, X, EMPTY]]))
print('\n')

"""
    RESULT
"""
print("----- RESULT -----")

# 1 -- Puts X in the first cell on empty board ✅
print("1 --", result(initial_state(), (0, 0)))

# 2 -- Puts O in the middle for active game ✅
board = [[X,     O,     X],
         [EMPTY, EMPTY, X],
         [O,     X,     O]]
action = (1, 1)
print("2 --", result(board, action))

# 3 -- doesn't alter the original array ✅
print("3 --")
print("Original board:     ", board)
applied = (result(board,action))
print("Board after result: ", board)



print('\n')

"""
    WINNER
"""
print("----- WINNER -----")

# 1 -- Returns O for winner in first row ✅
print("1 --", winner([[O, O, O], 
                      [X, X, O],  
                      [X, O, X]]))


# 2 -- Returns X for winner in center col ✅
print("2 --", winner([[O, X, O], 
                      [X, X, O],  
                      [O, X, X]]))

# 3 -- Returns O for winner in diagonal ✅
print("3 --", winner([[O, X, O], 
                      [X, O, X],  
                      [X, X, O]]))


# 4 -- Returns X for winner in diagonal ✅
print("4 --", winner([[O, X, X], 
                      [O, X, O],  
                      [X, X, O]]))

# 5 -- Returns None if no winner ✅
print("5 --", winner([[O, X, O], 
                      [O, X, X],  
                      [X, O, O]]))



print('\n')

"""
    WINNER
"""
print("----- TERMINAL -----")

# 1 -- Returns True for board with winner ✅
print("1 --", terminal([[O, O, O], 
                        [X, X, O],  
                        [X, O, X]]))

# 2 -- Returns True for board with winner and empty spaces ✅
print("2 --", terminal([[O, O, O], 
                        [X, X, O],  
                        [X, EMPTY, EMPTY]]))

# 3 -- Returns False for board with no winner and empty spaces ✅
print("3 --", terminal([[   O  , EMPTY,   O  ], 
                        [   X  ,   X  ,   O  ],  
                        [   X  , EMPTY, EMPTY]]))

# 3 -- Returns True for board with no winner and no empty spaces ✅
print("4 --", terminal([[O, X, O], 
                        [O, X, X],  
                        [X, O, O]]))



print('\n')

"""
    WINNER
"""
print("----- UTILITY -----")

# 1 -- Returns -1 when O is winner ✅
print("1 --", utility([[O, O, O], 
                      [X, X, O],  
                      [X, O, X]]))

# 2 -- Returns 1 when X is winner ✅
print("2 --", utility([[O, X, O], 
                      [X, X, O],  
                      [O, X, X]]))

# 2 -- Returns 0 if no winner ✅
print("3 --", utility([[O, X, O], 
                      [O, X, X],  
                      [X, O, O]]))