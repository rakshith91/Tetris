
def count_on_diagonals(board, row, col):
	diag_list=[]
	for x in range(0 , 2*N-1):
		forward_diag=[]
		backward_diag=[]
		for y in range(max(x-N+1, 0), min(x, N-1)+1):
			forward_diag.append(board[N-x+y-1][y])
			backward_diag.append(board[x-y][y])
			if N-x+y-1 == row and y== col:
				diag_list.append(forward_diag)
			if x-y == row and y == col:
				diag_list.append(backward_diag)
	return sum(diag_list[0])+sum(diag_list[1])-board[row][col]
