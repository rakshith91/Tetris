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
	a= [[(i,len(list(g))) for i,g in groupby(row)] for row in board]

def count_on_col(board):
	a= [[(i,len(list(g))) for i,g in groupby(col)] for col in zip(*board)]

def count_on_diag(board,n,k,color):
	count_list = []
	for r in range(0,n):
		for c in range(0,n):
			i=1
			count=0
			while board[r][c]==color and i<k:
				#right bottom diagonal
				if r+i<n and c+i<n and board[r+i][c+i]==color:
					count+=1
					print "1st",r,c,i,board[r][c],board[r+i][c+i]
				#left top diagonal
				if r-i>=0 and c-i>=0 and board[r-i][c-i]==color:
					count+=1
					print "2nd",r,c,i,board[r][c],board[r-i][c-i]
				#right top diagonal
				if r-i>=0 and c+i<n and board[r-i][c+i]==color:
					count+=1
					print "3rd",r,c,board[r-i][c+i]
				#left bottom diagonal
				if r+i<n and c-i>=0 and board[r+i][c-i]==color:
					count+=1
					print "4th",r,c,board[r+i][c-i]
				i+=1
			count_list.append(count)
	return sum(count_list)

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
	count_on_row(board)
	count_on_col(board)
	print count_on_diag(board,n,k,color)

#def solve(state):
color = determine_color(node)
successor= successors(string_to_board(node,n))
# for i in successor:
eval(successor[0],color,n,k)

