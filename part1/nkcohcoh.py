import sys
n = int(sys.argv[1])
k = int(sys.argv[2])
node = sys.argv[3]
time_limit = sys.argv[4]
def determine_color(node):
	whites = node.count('w')
	blacks = node.count('b')
	return 'w' if whites==blacks else 'b' if whites>blacks else "error"

def string_to_board(node, n):
	return [list(node[i:i+n]) for i in range(0, len(node), n)]		

def count_on_row(board, row, color):
	return sum(board[row])

def count_on_col(board,col):
	return sum([row[col] for row in board])

#def count_on_diagonals(board, row, col):
#idea for this function taken from assignment 0
def add_marble(board, row, col, color):
	return  board[0:row] + [board[row][0:col] + [color,] + board[row][col+1:]] + board[row+1:]

def successors(board):	
	return [add_marble(board, row, col, color) for row in range(0,n) for col in range(0,n) if board[row][col]=='.' ]
color= determine_color(node)
board= string_to_board(node,n)
print successors(board)

#def is_goal(board):

#def heuristic(state):

#def solve(state):
