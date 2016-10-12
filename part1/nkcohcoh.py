'''
1)write a function to check symmetry. we should not generate successors which are symmetrical to 
existing successors

2)write a function to check no of continuous w's , b's and .'s in a row, col and diagonal(assigned to Rakshith)

3) develop ( and code) a heuristic. 

4)write minimax / a*

PS: keep updating this.
'''
from copy import deepcopy
import sys
from itertools import groupby

n = int(sys.argv[1])
k = int(sys.argv[2])
node = sys.argv[3]
time_limit = sys.argv[4]

#determine which color takes the move. argument node is a string input from sys(refer line 4)
def determine_color(node):
	whites = node.count('w')
	blacks = node.count('b')
	return 'w' if whites==blacks else 'b' if whites>blacks else "error"

#converts the string input to a board (list of list) given n(line 2)
def string_to_board(node, n):
	return [list(node[i:i+n]) for i in range(0, len(node), n)]

#function incomplete
def count_on_row(board):
	return [[(i,len(list(g))) for i,g in groupby(row)] for row in board]

#function incomplete
def count_on_col(board):
	return [[(i,len(list(g))) for i,g in groupby(col)] for col in zip(*board)]

#def count_on_diagonals(board, row, col):


#idea for this function taken from assignment 0
def add_marble(board, row, col, color):
	return  board[0:row] + [board[row][0:col] + [color,] + board[row][col+1:]] + board[row+1:]

#successors for a given input. we should avoid symmetrical boards. so , we should write a function
#to check symmetry
def successors(board):	
	return [add_marble(board, row, col, color) for row in range(0,n) for col in range(0,n) if board[row][col]=='.' ]

#def is_goal(board):

def eval(board,color,n,k):
	print board,color
	print count_on_row(board)
	print count_on_col(board)
	count_on_diag(board,n)
	# 	row_count.append(count_on_row(board,row,color))
	# 	for col in range(0,n):
	# 		count_on_diag(board,row,col,n,k,color)
	# # col_count+=count_on_col(board,col,color)
	# for col in range(0,n):
	# 	col_count.append(count_on_col(board, col, color,col_count))

# https://d1b10bmlvqabco.cloudfront.net/attach/irnmu9v26th48r/irnn3xcxmhl79t/it989yrs3ja8/nqueens.py
def count_on_diag(board,N):
	diagonal1={}
	diagonal2={}
	for row in range(0,n):
		for col in range(0,n):
			dir=1
			diagonal1[(row,col)]=[board[r][c] for (r,c) in [(row - col * dir + c * dir, c) for c in range(0, N)] if r >= 0 and r < N]
			dir = -1
			diagonal2[(row, col)] =[board[r][c] for (r,c) in [(row - col * dir + c * dir, c) for c in range(0, N)] if r >= 0 and r < N]
	print diagonal1
	print diagonal2

# return sum(board[row])

# checks the symmetry
def check_symmetry(a,n):
	b = deepcopy(a)
	for col in range(0,n):
		for row in range(n-1,-1,-1):
			for row1 in range(0,n):
				for col1 in range(0,n):
					b[row1][col1]=a[col][row]
	print b

#def solve(state):
color = determine_color(node)
successor= successors(string_to_board(node,n))
# for i in successor:
eval(successor[0],color,n,k)

