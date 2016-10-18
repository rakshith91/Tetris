#Intial State- A board with black and white marbles placed on it in the format ..w.....b. The code determines the player who is supposed to play the next move
#Valid states- A set of successor states where a new marble of the current player is placed on the board
# Successor Function-Places a coloured marble of the current player on the board where no marble is placed
# Goal state- Next optimal move of the current player. A board state that adds a new marble in the most optimal position
#Heuristic function- The heuristic function subtracts the summation of the rows, columns and diagonals of the min player and the max player
# It returns the between those counts based on the turn of current player.

#Algorithm
#The code takes the value of n, k, a string displaying the current board input and time limit from the user.
#The code converts the string format to a board format
#The terminal state of the board is checked- This step verifies if the game is already won, already lost or there is a draw
#If the board is not a terminal state, then alpha beta pruning is applied to the entire tree to search for the next best possible outcome.
#A heuristic function is used to calculate the best state when the cut-off condition is satisfied.
#The time limit is checked while searching the entire tree. The time limit is adjusted to accomodate the pre-calculations.
#The resultant board showing the next best move is then converted to string and displayed to the user

#Problems Faced :
#The only problem we faced was coming up with a good heuristic function.

import sys
from itertools import groupby
import time
start_time = time.clock()

global count, color, utility_value, n, k

n = int(sys.argv[1]) #inputs the value of n
k = int(sys.argv[2]) # inputs the value of k
node = sys.argv[3]# Inputs the board state
time_limit = float(sys.argv[4]) #Inputs the time limit in seconds


# converts the string input to a board (list of list) given n(line 2)
def string_to_board(node, n):
    return [list(node[i:i + n]) for i in range(0, len(node), n)]

#Converts the board input to string input
def board_to_string(board):
    str = ''
    for row in board:
        for col in row:
            str += col
    return str


board = string_to_board(node, n)


# This function determines the player who is supposed to play next
#If white and black marbles are equal then its white players turn. If white marbles are more than the black marble then its blacks turn.
# If black marbles are more than white marble then its an error
def determine_color(node):
    whites = node.count('w')
    blacks = node.count('b')
    return 'w' if whites == blacks else 'b' if whites > blacks else "error"


color = determine_color(node)

# The add marble function adds black/white coloured marble to the board
def add_marble(board, row, col, color):
    return board[0:row] + [board[row][0:col] + [color, ] + board[row][col + 1:]] + board[row + 1:]

#The successor function adds a coloured marble to the board where there is no marble placed yet
def successors(board):
    color = determine_color(board_to_string(board))
    return [add_marble(board, row, col, color) for row in range(0, n) for col in range(0, n) if board[row][col] == '.']

#Counts the number of marbles in a row
def count_on_row(board):
    return [[(i, len(list(g))) for i, g in groupby(row)] for row in board]

#Counts the  number of marbles in a column
def count_on_col(board):
    return [[(i, len(list(g))) for i, g in groupby(col)] for col in zip(*board)]

#the idea of this function is taken from the nqueens code written by Prof. David Crandall
def generate_diag(board, n):
    diagonals1 = []
    diagonals2 = []
    for row in range(0, n):
        for col in range(0, n):
            if row != 0 and col == 0:
                # prints forward diagonals \ diagonals
                dir = 1
                diagonals1.append([board[r][c] for (r, c) in [(row - col * dir + c * dir, c) for c in range(0, n)] if
                                   r >= 0 and r < n])
            if row == 0:
                dir = 1
                diagonals1.append([board[r][c] for (r, c) in [(row - col * dir + c * dir, c) for c in range(0, n)] if
                                   r >= 0 and r < n])
                # prints backward diagonals / diagonals
                dir = -1
                diagonals2.append([board[r][c] for (r, c) in [(row - col * dir + c * dir, c) for c in range(0, n)] if
                                   r >= 0 and r < n])
            elif row != 0 and col == n - 1:
                dir = -1
                diagonals2.append([board[r][c] for (r, c) in [(row - col * dir + c * dir, c) for c in range(0, n)] if
                                   r >= 0 and r < n])
    d = diagonals1 + diagonals2
    return d


# def count_on_diag(d= generate_diag(board, n)):
def count_on_diag(diagonals):
    d = [i for i in diagonals if len(i) >= k]
    return [[(i, len(list(g))) for i, g in groupby(row)] for row in diagonals]

#Check if it's a terminal state if any of the players lose or if there is no place left to insert a marble
def is_terminal(board, k, color):
    # check if there's no space on the board
    if len([col for row in board for col in row if col == '.']) == 0:
        return True

    # check if there's a line in the column
    result = [c for r in count_on_col(board) for c in r if c[1] == k and c[0] == color]
    if result:
        return True
    result = [c for r in count_on_row(board) for c in r if c[1] == k and c[0] == color]
    if result:
        return True

    # check if there's a line in the diagonal
    result = [c for r in count_on_diag(generate_diag(board, n)) for c in r if c[1] == k and c[0] == color]
    if result:
        return True
    return False


# Heuristic which decides the min-max value of current state when cut-off condition turns True
# The heuristics check for number of consecutive blacks/white pebbles in row, column and diagonals.
# The heuristic function subtracts the summation of the rows, columns and diagonals of the min player and the max player
# It returns the between those counts based on the turn of current player.

def heur(board, color):
    white_list = 0
    black_list = 0
    for row in board:
        x = [row[i:i + k] for i in range(0, n - k + 1)]
        for i in x:
            if 'b' not in i:
                white_list += 1
            if 'w' not in i:
                black_list += 1
    for col in zip(*board):
        x = [col[i:i + k] for i in range(0, n - k + 1)]
        for i in x:
            if 'b' not in i:
                white_list += 1
            if 'w' not in i:
                black_list += 1
    for element in generate_diag(board, n):
        x = filter(None, [element[i:i + k] if len(element[i:i + k]) >= k else None for i in range(0, n - k + 1)])
        for i in x:
            if 'b' not in i:
                white_list += 1
            if 'w' not in i:
                black_list += 1
    return black_list - white_list if color == 'b' else white_list - black_list


# Utility function to determine the min-max value of the given state
def utility(board, color):
    # check if color wins/looses in row
    result = [c for r in count_on_row(board) for c in r if c[1] == k and c[0] == color]
    if result:
        return -1
    result = [c for r in count_on_row(board) for c in r if c[1] == k and c[0] != color]
    if result:
        return 1

    # check if color wins/looses in col
    result = [c for r in count_on_col(board) for c in r if c[1] == k and c[0] == color]
    if result:
        return -1
    result = [c for r in count_on_col(board) for c in r if c[1] == k and c[0] != color]
    if result:
        return 1

    # check if color wins/looses in diagonal
    result = [c for r in count_on_diag(generate_diag(board, n)) for c in r if c[1] == k and c[0] == color]
    if result:
        return -1
    result = [c for r in count_on_diag(generate_diag(board, n)) for c in r if c[1] == k and c[0] != color]
    if result:
        return 1

    # check for a draw
    if len([col for row in board for col in row if col == '.']) == 0:
        return 0


# MIN function with alpha beta pruning
def min_player(board, k, color, count,  alpha, beta):
    #Cut-off test
    #The recursion gets exit when time limit exceeds or the terminal is reached
    if is_terminal(board, k, color) or (time.clock() - start_time >= time_limit-0.5):  #Adjusting time limit check to accomodate pre-calculations
        utility_val = heur(board, determine_color(board_to_string(board)))
        return utility_val
    else:
        count += 1
        min_array = [max_player(s, k, color, count, alpha, beta) for s in successors(board)]
        v = min(min_array)
        # Compares the current utility value with alpha value to check if it didn't fall below the alpha value
        if v <= alpha:
            return v
        beta = min(beta, v)
        return v

#MAX function with alpha beta pruning
def max_player(board, k, color, count,alpha, beta):
    # Cut-off test
    # The recursion gets exit when time limit exceeds or the terminal is reached
    if is_terminal(board, k, color) or (time.clock() - start_time >= time_limit-0.5): #Adjusting time limit check to accomodate pre-calculations
        utility_val = heur(board, determine_color(board_to_string(board)))
        return utility_val
    else:
        count += 1
        max_array = [min_player(s, k, color, count, alpha, beta) for s in successors(board)]
        v = max(max_array)
        # Compares the current utility value with beta value to check if it didn't exceed the beta value
        if v >= beta:
            return v
        alpha = max(alpha, v)
        return v

#board_to_string function converts the board to string
def board_to_string(board):
    str = ''
    for row in board:
        for col in row:
            str += col
    return str

# The code starts executing from below:

utility_value = -9999
resultant_board = []
count = 0

if is_terminal(board, k, color):
    util = utility(board, color)
    if util == 1:
        print color, " has already won the game"
    elif util == -1:
        print color, " has already lost the game"
    elif util == 0:
        print "the game is already a draw"
    else:
        print "errored input"
else:
    utility_value = -9999
    count += 1
    for s in successors(board):
        if is_terminal(s, k, color):
            uv = heur(s, determine_color(board_to_string(s)))

        else:
            uv = min_player(s, k, color, count,-float("inf"),float("inf"))

        if uv > utility_value:
            utility_value = uv
            resultant_board = s
result=board_to_string(resultant_board)

print result
