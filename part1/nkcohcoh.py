import sys
from itertools import groupby

n = int(sys.argv[1])
k = int(sys.argv[2])
node = sys.argv[3]
time_limit = sys.argv[4]

#converts the string input to a board (list of list) given n(line 2)
def string_to_board(node, n):
	return [list(node[i:i+n]) for i in range(0, len(node), n)]

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
	return [add_marble(board, row, col, color) for row in range(0,n) for col in range(0,n) if board[row][col]=='.' ]

def count_on_row(board):
	return [[(i,len(list(g))) for i,g in groupby(row)] for row in board]

def count_on_col(board):
	return [[(i,len(list(g))) for i,g in groupby(col)] for col in zip(*board)]

def generate_diag(board,n):
	print "board",board
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
    print result, "resu"
    if result:
        print c[0], "lost"
        # return (True, c[0])
        return True
    # check if there's a line in a row
    result = [c for r in count_on_row(board) for c in r if c[1] == k and c[0] == color]
    if result:
        print result, "row"
        # return (True, c[0])
        return True

    #check if there's a line in the diagonal
    result = [c for r in count_on_diag() for c in r if c[1] == k and c[0] == color]
    if result:
        print result, "di"
        # return (True, c[0])
        return True
    return False

def utility(board,color):
    #check if color wins/looses in row
    result = [c for r in count_on_row(board) for c in r if c[1] == k and c[0] == color]
    if result:
        return 1
    result = [c for r in count_on_row(board) for c in r if c[1] == k and c[0] != color]
    if result:
        return -1

    #check if color wins/looses in col
    result = [c for r in count_on_col(board) for c in r if c[1] == k and c[0] == color]
    if result:
        return 1
    result = [c for r in count_on_col(board) for c in r if c[1] == k and c[0] != color]
    if result:
        return -1

    #check if color wins/looses in diagonal
    result = [c for r in count_on_diag() for c in r if c[1] == k and c[0] == color]
    if result:
        return 1
    result = [c for r in count_on_diag() for c in r if c[1] == k and c[0] != color]
    if result:
        return -1

    #check for a draw
    if len([col for row in board for col in row if col == '.'])==0:
        return 0

def min(board):
    if is_terminal(board,k,color):
        print "min ended"
        return -1
    else:
        # return util(board)
        # min([max(s) for s in successors(board)])
        print [max(s) for s in successors(board)]

def max(board):
    if is_terminal(board,k,color):
        print "max ended"
        return 1
    else:
        # return util(board)
        # max([min(s) for s in successors(board)])
        print [min(s) for s in successors(board)]

successor_array=[]
utility_value=-9999
resultant_board=[]
for s in successors(board):
    uv=max(board)
    if uv<utility_value:
        utility_value=uv
        resultant_board=s
print resultant_board