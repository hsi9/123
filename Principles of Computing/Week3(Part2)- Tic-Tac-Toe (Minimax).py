"""
Mini-max Tic-Tac-Toe Player
"""

import poc_ttt_gui
import poc_ttt_provided as provided
import random
# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    mm_move_list = []
    #temp_board = board.clone()
    if board.check_win() == None:
        #mm_move_list = []
        for choice in board.get_empty_squares():
            temp_board = board.clone()
            temp_board.move(choice[0], choice[1], player)
            score, dummy_position = mm_move(temp_board, provided.switch_player(player))
            if score * SCORES[player] == 1:
                return score, choice
            else:
                mm_move_list.append((score * SCORES[player], choice))
        max_score = max(mm_move_list)[0]
        best_moves = [item for item in mm_move_list if item[0] == max_score]
        best_move = random.choice(best_moves)
        return best_move[0]*SCORES[player], best_move[1]
    else:
        return SCORES[board.check_win()], (-1, -1)
      
    return 0, (-1, -1)

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)
