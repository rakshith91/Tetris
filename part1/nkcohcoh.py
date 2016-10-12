''' TO DO
1)write a function to check symmetry. we should not generate successors which are symmetrical to 
existing successors

2)write a function to check no of continuous w's , b's and .'s in a row, col and diagonal(assigned to Rakshith)

3) develop ( and code) a heuristic. 

4)write minimax / a*

PS: keep updating this.

'''


from itertools import groupby
import sys
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

#counts continous values of whites and blacs and dots in all row
def count_on_row(board):
	return [[(i,len(list(g))) for i,g in groupby(row)] for row in board]

#counts continous values of whites and blacs and dots in all cols
def count_on_col(board):
	 return [[(i,len(list(g))) for i,g in groupby(col)] for col in zip(*board)]

#counts continous values of whites , blacks and dots in all diagonals
#def count_on_diagonals(board):


#idea for this function taken from assignment 0
def add_marble(board, row, col, color):
	return  board[0:row] + [board[row][0:col] + [color,] + board[row][col+1:]] + board[row+1:]

#successors for a given input. we should avoid symmetrical boards. so , we should write a function
#to check symmetry


def successors(board):	
	return [add_marble(board, row, col, color) for row in range(0,n) for col in range(0,n) if board[row][col]=='.' ]

#def is_goal(board):

#def heuristic(state):

#def solve(state):
