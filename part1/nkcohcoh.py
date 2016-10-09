import sys
n = int(sys.argv[1])
k = int(sys.argv[2])
node = sys.argv[3]
time_limit = sys.argv[4]

def string_to_board(node, n):
	return [list(node[i:i+n]) for i in range(0, len(node), n)]		

print string_to_board(node, n)
#def is_goal(board):

#def add_black_marble(board, row, col):

#def add_white_marble(board, row, col):

#def successors(state):
#
#def heuristic(state):
#
#def solve(state):
