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


# David Crandal's nqueens code
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
	return 0

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

def possible_row(board):
	return [i for i in board]

def possible_col(board):
	return [col for col in zip(*board)] #Rakshit please explain me how zip works and what does *board mean


#incomplete function
def eval(data_structure,n,k):
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


color = determine_color(node)
board = string_to_board(node, n)
data_structure = [board,'MIN']
eval(data_structure,n,k)

#Algorithm for Minimax - wikipedia


# function minimax(node, depth, maximizingPlayer)
#      if depth = 0 or node is a terminal node
#          return the heuristic value of node
#
#      if maximizingPlayer
#          bestValue := −∞
#          for each child of node
#              v := minimax(child, depth − 1, FALSE)
#              bestValue := max(bestValue, v)
#          return bestValue
#
#      else    (* minimizing player *)
#          bestValue := +∞
#          for each child of node
#              v := minimax(child, depth − 1, TRUE)
#              bestValue := min(bestValue, v)
#          return bestValue


# is_goal(board,k)
# count_on_diag(board,n)
#
# this is how i think algo should be:
def minimax(data_structure,n,k):

	#identify MIN and MAX Players
	MAX = determine_color(board)
	if MAX=='b':
		MIN='w'
	else:
		MIN='b'

	while fringe!=0:
		if is_goal(board,k):	#this function will return the data structure ie. [[board],e,MAX/MIN]
			print MAX/MIN lost
			return 0
# 	else:
# 		s=successor(board,MAX)
# 		for each S:
# 			calculate eval(s) and append on the board
# 			if MAX:
# 				choose minimum out of (e)
# 				successor(board,MIN)
# 			elif MIN:
# 				choose maximum out of (e)
# 				successor(board,MAX)
#
# #
# def minimax_decision(s):
# 	#Return action leading to state SSUCC(S) that maximizes MIN_Value(S)
#
# def maxvalue(s):
# 	'''If Terminal ?(s) return result(s)
# 	else return max of s' which belongs to successor of s min_value(s')
# 	'''
#
# def minvalue(s):
# 	if terminal ? (s) return result(s)
# 	else return min of s' max_value(s')

