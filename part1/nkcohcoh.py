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

def count_on_row(board):
	return [[(i,len(list(g))) for i,g in groupby(row)] for row in board]

def count_on_col(board):
	return [[(i,len(list(g))) for i,g in groupby(col)] for col in zip(*board)]

def count_on_diag(board,n):
	print "board",board
	diagonals1=[]
	diagonals2=[]
	for row in range(0,n):
		for col in range(0,n):
			dir=1
			diagonals1.append( [ board[r][c] for (r,c) in [ (row-col*dir+c*dir,c) for c in range(0,n) ] if r >= 0 and r < n ])
			dir=-1
			diagonals2.append([ board[r][c] for (r,c) in [ (row-col*dir+c*dir,c) for c in range(0,n) ] if r >= 0 and r < n ])
	d=diagonals1+diagonals2
	return [(key, len(list(group))) for i in d for key,group in groupby(i)]

#idea for this function taken from assignment 0
def add_marble(board, row, col, color):
	return  board[0:row] + [board[row][0:col] + [color,] + board[row][col+1:]] + board[row+1:]

#successors for a given input. we should avoid symmetrical boards. so , we should write a function
#to check symmetry
def successors(board):	
	return [add_marble(board, row, col, color) for row in range(0,n) for col in range(0,n) if board[row][col]=='.' ]

def is_goal(board,k):
	#loss by column
	result= list(set([c[0] for r in count_on_col(board) for c in r if c[1]==k and c[0]!='.']))
	if result:
		print result[0][0],"lost by column"
		return 1
	result= list(set([c for r in count_on_row(board) for c in r if c[1]==k and c[0]!='.']))
	if result:
		print result[0][0], "lost by row"
		return 1
	result = list(set([r[0] for r in count_on_diag(board, n) if r[1]==k and r[0]!='.']))
	if result:
		print result[0],"lost by diagonal"
		return 1

def eval(board,color,n,k):
	print board,color
	count_on_row(board,color)
	count_on_col(board)
	print count_on_diag(board,n,k,color)

def solve(board,color):
    fringe=[board]
    while len(fringe)>0:
        valid_state=fringe.pop()
        for s in successors(valid_state,color):
			for clr in range(0,1):
				if color!=clr:
					solve(s,clr)

def color_num(color):
	if color=='w':
		return 1
	elif color=='b':
		return 0

color = determine_color(node)
# color = color_num(color)
print color
board = string_to_board(node, n)
is_goal(board,n)
# print board
# fringe = []
# Solution = solve(board, color)


