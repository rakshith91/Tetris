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
color = determine_color(node)

#define max and min
max=color
if max=='b':
	min='w'
else:
	min='b'

#converts the string input to a board (list of list) given n(line 2)
def string_to_board(node, n):
	return [list(node[i:i+n]) for i in range(0, len(node), n)]

def count_on_row(board):
	return [[(i,len(list(g))) for i,g in groupby(row)] for row in board]

def count_on_col(board):
	return [[(i,len(list(g))) for i,g in groupby(col)] for col in zip(*board)]

board = string_to_board(node, n)
	
# https://d1b10bmlvqabco.cloudfront.net/attach/irnmu9v26th48r/irnn3xcxmhl79t/it989yrs3ja8/nqueens.py
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

print count_on_diag()

#idea for this function taken from assignment 0
def add_marble(board, row, col, color):
	return  board[0:row] + [board[row][0:col] + [color,] + board[row][col+1:]] + board[row+1:]

#successors for a given input. we should avoid symmetrical boards. so , we should write a function
#to check symmetry
def successors(board):	
	return [add_marble(board, row, col, color) for row in range(0,n) for col in range(0,n) if board[row][col]=='.' ]



def is_goal(board,k,color):
	result= [c for r in count_on_col(board) for c in r if c[1]==k and c[0]==color]
	print result,"resu"
	if result:
		print c[0],"lost"
		return (True, c[0])
	result= [c for r in count_on_row(board) for c in r if c[1]==k and c[0]==color]
	if result:
		print result,"row"
		return (True, c[0])
	
	result = [c for r in count_on_diag() for c in r if c[1]==k and c[0]==color]
	if result:
		print result,"di"
		return (True, c[0])
	return False

is_goal(board,k,max,min)


print solve(board, determine_color(node))
def color_num(color):
	if color=='w':
		return 1
	elif color=='b':
		return 0

def assign_score(board, color=color):
	if is_goal(board, k)[0] and is_goal(board, k)[1]!=color:
		return 1
	elif is_goal(board, k)[0] and is_goal(board, k)[1]==color:
		return -1
	elif not is_goal(board, k)[0] :
		return 0

print assign_score(board, color)
#def possible_row(board):
#	return [i for i in board]
#
#def possible_col(board):
#	return [col for col in zip(*board)] #Rakshit please explain me how zip works and what does *board mean


#incomplete function
def heuristic(data_structure,n,k):
	if data_structure[1]=='MAX':
		print data_structure[0]
		#do the same thing what is in down
	elif data_structure[1]=='MIN':

		print "data structure is ",data_structure[0]

		pos_row = possible_row(board)
		min_loss_row = len([x for x in pos_row if 'w' not in x])
		max_loss_row = len([x for x in pos_row if 'b' not in x])
		print max_loss_row, min_loss_row
		print "min_loss_rows",[x for x in pos_row if 'w' not in x]
		print "max_loss_rows", [x for x in pos_row if 'b' not in x]

		pos_col = possible_col(board)
		min_loss_col= len([x for x in pos_col if 'w' not in x])
		max_loss_col= len([x for x in pos_col if 'b' not in x])
		print max_loss_col,min_loss_col
		print "min_loss_col", [x for x in pos_col if 'w' not in x]
		print "max loss col", [x for x in pos_col if 'b' not in x]

		all_diagonals=generate_diag(data_structure[0],n)
		print "all diag",all_diagonals
		possible_diagonals = [i for i in all_diagonals if len(i)>=k]
		print "possible diag",possible_diagonals
		min_loss_diag=len([x for x in possible_diagonals if 'w' not in x])
		max_loss_diag=len([x for x in possible_diagonals if 'b' not in x])
		print max_loss_diag,min_loss_diag

		e=(max_loss_row+max_loss_col+max_loss_diag)-(min_loss_row+min_loss_col+min_loss_diag)
		# # find the diagonals with only w and . (max_loss)
		# # find the diagonals with only b and . (min loss)
		# # e=max loss - min loss
		print e

def solve(board,color):
	fringe=[board]
	while fringe:
		for s in successors(fringe.pop()):
			if is_goal(s,k):
				return s
			fringe.append(s)
	return False

def minimax_decision(board):
	if is_goal(board,k):
		print "eureka jeet gae"
	else:
		s=successors(board)
