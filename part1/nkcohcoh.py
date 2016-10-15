import sys
from itertools import groupby

n = int(sys.argv[1])
k = int(sys.argv[2])
node = sys.argv[3]
time_limit = sys.argv[4]

#converts the string input to a board (list of list) given n(line 2)
def string_to_board(node, n):
	return [list(node[i:i+n]) for i in range(0, len(node), n)]

def board_to_string(board):
	str=''
	for row in board:
		for col in row:
			str+=col
	return str

board=string_to_board(node,n)
print board

def determine_color(node):
	whites = node.count('w')
	blacks = node.count('b')
	return 'w' if whites==blacks else 'b' if whites>blacks else "error"
color = determine_color(node)

print color

#idea for this function taken from assignment 0
def add_marble(board, row, col, color):
	return  board[0:row] + [board[row][0:col] + [color,] + board[row][col+1:]] + board[row+1:]
	# return board[0:row] + [board[row][0:col] + [color, ] + board[row][col + 1:]] + board[row + 1:]


def successors(board):
	color=determine_color(board_to_string(board))
	return [add_marble(board, row, col, color) for row in range(0,n) for col in range(0,n) if board[row][col]=='.' ]

# print successors([['w', 'w', '.'], ['b', '.', 'b'], ['b', 'w', 'w']])

def count_on_row(board):
	return [[(i,len(list(g))) for i,g in groupby(row)] for row in board]

def count_on_col(board):
	return [[(i,len(list(g))) for i,g in groupby(col)] for col in zip(*board)]

def generate_diag(board,n):
	diagonals1=[]
	diagonals2=[]
	for row in range(0,n):
		for col in range(0,n):
			if row!=0 and col==0:
				dir=1
				diagonals1.append( [ board[r][c] for (r,c) in [ (row-col*dir+c*dir,c) for c in range(0,n) ] if r >= 0 and r < n ])
				# print "forward diagonals \ ",diagonals1
			if row==0:
				dir = 1
				diagonals1.append([board[r][c] for (r, c) in [(row - col * dir + c * dir, c) for c in range(0, n)] if r >= 0 and r < n])
				# print "forward diagonals \ "
				dir=-1
				diagonals2.append([ board[r][c] for (r,c) in [ (row-col*dir+c*dir,c) for c in range(0,n) ] if r >= 0 and r < n ])
				# print "backward diagonals / ",diagonals2
			elif row!=0 and col==n-1:
				dir = -1
				diagonals2.append([board[r][c] for (r, c) in [(row - col * dir + c * dir, c) for c in range(0, n)] if r >= 0 and r < n])
				# print "backward diagonals / " , diagonals2
	d = diagonals1 + diagonals2
	return d

def count_on_diag(d= generate_diag(board, n)):
	d= [i for i in d if len(i)>=k]
	return [[(i,len(list(g))) for i,g in groupby(row)] for row in d]

def is_terminal(board, k, color):
	#check if there's no space on the board
	if len([col for row in board for col in row if col == '.'])==0:
		print "terminal state"
		return True

	#check if there's a line in the column
	result = [c for r in count_on_col(board) for c in r if c[1] == k and c[0] == color]
	if result:
		print c[0], "lost"
		return True
	result = [c for r in count_on_row(board) for c in r if c[1] == k and c[0] == color]
	if result:
		print result, "row"
		return True

	#check if there's a line in the diagonal
	result = [c for r in count_on_diag() for c in r if c[1] == k and c[0] == color]
	if result:
		print result, "di"
		return True
	return False

# print is_terminal([['w', 'w', 'b'], ['b', 'w', 'b'], ['b', 'w', 'w']],k,color)

def utility(board,color):
    #check if color wins/looses in row
    result = [c for r in count_on_row(board) for c in r if c[1] == k and c[0] == color]
    if result:
        return -1
    result = [c for r in count_on_row(board) for c in r if c[1] == k and c[0] != color]
    if result:
        return 1

    #check if color wins/looses in col
    result = [c for r in count_on_col(board) for c in r if c[1] == k and c[0] == color]
    if result:
        return -1
    result = [c for r in count_on_col(board) for c in r if c[1] == k and c[0] != color]
    if result:
        return 1

    #check if color wins/looses in diagonal
    result = [c for r in count_on_diag() for c in r if c[1] == k and c[0] == color]
    if result:
        return -1
    result = [c for r in count_on_diag() for c in r if c[1] == k and c[0] != color]
    if result:
        return 1

    #check for a draw
    if len([col for row in board for col in row if col == '.'])==0:
        return 0

# print utility([['b', 'b', 'b'], ['w', '.', 'w'], ['w', '.', '.']],'w')

def min_player(board,k,color):
	print "this board entered min ", board
	if is_terminal(board,k,color):
		utility_val=utility(board,color)
		print "utility_val is ",utility_val
		return utility_val
	else:
		min_array=[max_player(s,k,color) for s in successors(board)]
		print "min array is ",min_array
		return min(min_array)

def max_player(board,k,color):
	print "this board entered max ",board
	if is_terminal(board,k,color):
		utility_val = utility(board, color)
		print "utility_val is ",utility_val
		return utility_val
	else:
		max_array=[min_player(s,k,color) for s in successors(board)]
		print "max array is ",max_array
		return max(max_array)

utility_value=-9999
resultant_board=[]
for s in successors(board):
	print "s is ",s
	uv=max_player(s,k,color)
	print "uv is ",uv
	if uv>utility_value:
		utility_value=uv
		print "utility value changed to",utility_value
		resultant_board=s
print resultant_board