# Simple tetris program! v0.2
# D. Crandall, Sept 2016

from AnimatedTetris import *
from SimpleTetris import *
from kbinput import *
import time, sys
from copy import deepcopy
class HumanPlayer:
	def get_moves(self, tetris):
		print "Type a sequence of moves using: \n  b for move left \n  m for move right \n	n for rotation\nThen press enter. E.g.: bbbnn\n"
		moves = raw_input()
		return moves

	def control_game(self, tetris):
		while 1:
			c = get_char_keyboard()
			commands =	{ "b": tetris.left, "n": tetris.rotate, "m": tetris.right, " ": tetris.down }
			commands[c]()

#####
# This is the part you'll want to modify!
# Replace our super simple algorithm with something better
#
class ComputerPlayer:
	# This function should generate a series of commands to move the piece into the "optimal"
	# position. The commands are a string of letters, where b and m represent left and right, respectively,
	# and n rotates. tetris is an object that lets you inspect the board, e.g.:
	#	- tetris.col, tetris.row have the current column and row of the upper-left corner of the 
	#	  falling piece
	#	- tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
	#	- tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
	#	  issue game commands
	#	- tetris.get_board() returns the current state of the board, as a list of strings.
	#
	#awards if a successor clears a line	
	def clears(self, board):
		count=0
		for row in board:
			if row == 'xxxxxxxxxx':
				count+=1		
		return count

	#base reward: reward if a piece touches the base
	def base_reward(self, succ):	
		base_reward_list=[]
		for item in succ:
			board = item[0]
			base_reward_list.append((board[-1].count('x'), item[1]))

		return base_reward_list
			

	#edge reward: reward if a piece touches edges
	def edge_reward(self, succ):
		reward_list=[]
		for item in succ:
			x= item[0]
			board = zip(*x)
			reward_list.append((board[0].count('x')+board[-1].count('x'), item[1]))
		return reward_list

	def get_possible_moves(self,current_col):
		moves=[]
		for i in range(1, current_col+1):
			moves.append("b"*i)
			moves.append("n"+"b"*i)
			moves.append("nn"+"b"*i)
			moves.append("nnn"+"b"*i)
		for i in range(0, 10-current_col):	
			moves.append("m"*i)
			moves.append("n"+"m"*i)
			moves.append("nn"+"m"*i)
			moves.append("nnn"+"m"*i)
		return moves
	
	def get_positions(self, board):
		
		b= zip(*board)
		ind_list=[]
		col_no=0
		for col in b:
			lcol= list(col)
			if 'x' in lcol:
				ind_list.append((col_no,lcol.index('x')))
			else:
				ind_list.append((col_no,20))
			col_no+=1
		return ind_list
	
	def successors(self,board,piece,piece_col, score):		
		#brd = ['         '*20]
		#print self.get_positions(brd),"her"
		temp_obj= TetrisGame()
		#piece= temp_obj.get_piece()[0]
		temp_board=board
		positions= self.get_positions(temp_board)
		print positions,"pos"
		possible_rotations=[]
		possible_rotations.append(piece)		
		possible_rotations.append(temp_obj.rotate_piece(piece,90))
		possible_rotations.append(temp_obj.rotate_piece(piece,180))
		possible_rotations.append(temp_obj.rotate_piece(piece,270))
		successor_list=[]
		for piece in possible_rotations: 
			move=""
			if possible_rotations.index(piece)==1:
				move+="n"
			elif possible_rotations.index(piece)==2:
				move+="nn"
			elif possible_rotations.index(piece)==3:
				move+="nnn"
			piece_height = len(piece)
			piece_width= len(max(piece, key=len))
			for element in positions:
				if not TetrisGame.check_collision((board, score),piece,element[1]-piece_height,element[0]):	
					if element[0]+piece_width<=10:
						new_board = TetrisGame().place_piece((temp_board, score), piece,element[1]-piece_height ,element[0])
						if element[0]<piece_col:
							successor_list.append((new_board[0], move+"b"*(piece_col-element[0])))
						elif element[0]>piece_col:
							successor_list.append((new_board[0], move+"m"*(element[0]-piece_col)))
						elif element[0]==piece_col:
							successor_list.append((new_board[0], move))
						#print "newboard", new_board
		return successor_list
	
	def calculate_penalty(self, board, piece, piece_col, score):
		succ= self.successors(board, piece, piece_col, score)
		base=self.base_reward(succ) 
		edge = self.edge_reward(succ)
		height= self.height_penalty(succ)
		penalty_list=[]
		for i in range(len(succ)):
			move= succ[i]
			penalty_list.append((-4*(height[i][0]), move))
		sorted_list= sorted(penalty_list,key=lambda tup:tup[0] , reverse=True)
		return sorted_list[0]
		
		
	#calculates penalty for height
	def height_penalty(self,succ):
		#succ= self.successors(board, piece, piece_col, score)
		height_penalty=[]
		for board in succ:
			item = board[0]
			item.reverse()
			count=0
			for row in item:
				count += row.count('x')
			height_penalty.append((count, board[1]))
		return height_penalty
	def height(self, board):
		x_list=[]
		for row in board:
			if 'x' in row:
				x_list.append(board.index(row))	
		return min(x_list) if x_list else 0
	
	def calculate_height(self, board,piece,piece_col, score):	
		current_height= self.height(board)
   		succ = self.successors(board,piece,piece_col,score)	
		#print succ, "successors"
		height_list=[]
		for item in succ:
			#print item, "item"
			move= item[1]
			new_board = item[0]
			height_list.append((self.height(new_board)- current_height,move))
		sorted_list = sorted(height_list, key=lambda tup:tup[0])
		print sorted_list, "sl"
		return sorted_list[-1]
	
	def holes(self, board):
		return board	
	def calculate_holes(self, board, piece, piece_col, score):
		succ = self.successors(board,piece,piece_col,score)
		return board

			
	def get_moves(self, tetris):
		temp= TetrisGame()	
		brd = tetris.get_board()
		current_col= tetris.col
		piece= tetris.get_piece()[0]
		piece_col= tetris.get_piece()[2]
		row =tetris.row
		col= tetris.col
		#print self.get_positions(board)
		score = temp.get_score()
		moves= self.get_possible_moves(current_col)
		#self.successors(board,piece,score)
		temp_board= deepcopy(brd)
		print brd 
		succ= self.calculate_height(temp_board, piece,piece_col, score)
		print succ, "succcc"
		
		return succ[1]
	   
	# This is the version that's used by the animted version. This is really similar to get_moves,
	# except that it runs as a separate thread and you should access various methods and data in
	# the "tetris" object to control the movement. In particular:
	#	- tetris.col, tetris.row have the current column and row of the upper-left corner of the 
	#	  falling piece
	#	- tetris.get_piece() is the current piece, tetris.get_next_piece() is the next piece after that
	#	- tetris.left(), tetris.right(), tetris.down(), and tetris.rotate() can be called to actually
	#	  issue game commands
	#	- tetris.get_board() returns the current state of the board, as a list of strings.
	#
	def control_game(self, tetris):
		# another super simple algorithm: just move piece to the least-full column
		while 1:
			time.sleep(0.1)

			board = tetris.get_board()
			column_heights = [ min([ r for r in range(len(board)-1, 0, -1) if board[r][c] == "x"  ] + [100,] ) for c in range(0, len(board[0]) ) ]
			index = column_heights.index(max(column_heights))

			if(index < tetris.col):
				tetris.left()
			elif(index > tetris.col):
				tetris.right()
			else:
				tetris.down()


###################
#### main program

(player_opt, interface_opt) = sys.argv[1:3]

try:
	if player_opt == "human":
		player = HumanPlayer()
	elif player_opt == "computer":
		player = ComputerPlayer()
	else:
		print "unknown player!"

	if interface_opt == "simple":
		tetris = SimpleTetris()
	elif interface_opt == "animated":
		tetris = AnimatedTetris()
	else:
		print "unknown interface!"

	tetris.start_game(player)

except EndOfGame as s:
	print "\n\n\n", s



