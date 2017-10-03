# This will be the best version of the bot using all methods from other scripts and combining them
import flowFreeBot
import recursive_solver
import pyautogui
import time
import numpy

def main():
	dimensions_of_board = (30, 170, 470, 610)
	while(True):
		original_board = flowFreeBot.capture_board(dimensions_of_board)
		size_of_board = flowFreeBot.vertical_line_detector(original_board)
		print('You are playing a {} x {} board'.format(size_of_board, size_of_board))
		size_of_square = (dimensions_of_board[2]-dimensions_of_board[0])/size_of_board
		board_of_pixels = flowFreeBot.create_pixel_board(dimensions_of_board, size_of_board, size_of_square)
		board_of_colours = flowFreeBot.create_colour_board(board_of_pixels, size_of_board)
		print(board_of_colours)
		# save the initial board of colours as the head of our tree
		# next generate all the children of the parent and add these as branches to some data structure
		# next pass all these children into is_solved() and if any return True then we have a solution
		# if not then generate a new generation of children using all our current children as the parents (this will grow exponentially and need serious optimisation)
		start = time.time()
		solved_board = recurse_solve(board_of_colours)
		print('time taken was {} seconds'.format(time.time()-start))
		print(solved_board)
		list_of_array_of_moves = flowFreeBot.move_finder(solved_board, board_of_colours, size_of_board)
		flowFreeBot.draw_solution(board_of_pixels, list_of_array_of_moves)
		time.sleep(1)
		pyautogui.moveTo(250,370)#move to next level
		pyautogui.click() #click next level
		time.sleep(1)

def recurse_solve(board):
	#print(board, '\n')
	#board = flowFreeBot.solveboard(board, board.shape[0]).copy()
	#print(board, '\n')
	#time.sleep(1)
	characters_that_are_ends = ['b', 'r', 'g', 'y', 'o', 'p', 'z', 'c', 't', 'd', 'q', 's', 'l', 'm', 'w', 'a']
	for i in range(board.shape[0]):
		for j in range(board.shape[1]):
			if board[i,j] in characters_that_are_ends:
				try:
					if i > 0:
						if board[i-1,j] == board[i,j]:
							board[i-1,j] = board[i,j].upper()
							board[i,j] = board[i,j].upper()
				except IndexError as e:
					pass
				try:
					if board[i+1,j] == board[i,j]:
						board[i+1,j] = board[i,j].upper()
						board[i,j] = board[i,j].upper()
				except IndexError as e:
					pass
				try:
					if j > 0:
						if board[i,j-1] == board[i,j]:
							board[i,j-1] = board[i,j].upper()
							board[i,j] = board[i,j].upper()
				except IndexError as e:
					pass
				try:
					if board[i,j+1] == board[i,j]:
						board[i,j+1] = board[i,j].upper()
						board[i,j] = board[i,j].upper()
				except IndexError as e:
					pass
	if recursive_solver.is_solved(board):
		return(board)
	elif recursive_solver.pass_constraints_check(board):
		for possible_board in find_possible_moves(board):
			temp = recurse_solve(possible_board)
			if temp is not None:
				return temp

def find_possible_moves(board): # this will take in a board and returna list of all the possible boards this one could be in 1 move
	characters_that_are_ends = ['b', 'r', 'g', 'y', 'o', 'p', 'z', 'c', 't', 'd', 'q', 's', 'l', 'm', 'w', 'a']
	colour_to_look_for = []
	elements_in_board = numpy.unique(board)
	try:
		elements_in_board.remove('0')
	except:
		pass
	for colour in elements_in_board:
		if colour in characters_that_are_ends:
			colour_to_look_for.append(colour)
			break
	list_of_boards = []
	for i in range(board.shape[0]):
		for j in range(board.shape[0]):
			if board[i,j] in colour_to_look_for:
				try:
					if board[i+1,j] == '0':
						temp = board.copy()
						temp[i+1,j] = board[i,j]
						temp[i,j] = temp[i,j].upper()
						list_of_boards.append(temp)
				except IndexError as e:
					pass
				try:
					if i > 0:
						if board[i-1,j] == '0':
							temp = board.copy()
							temp[i-1,j] = board[i,j]
							temp[i,j] = temp[i,j].upper()
							list_of_boards.append(temp)
				except IndexError as e:
					pass
				try:
					if j > 0:
						if board[i,j-1] == '0':
							temp = board.copy()
							temp[i,j-1] = board[i,j]
							temp[i,j] = temp[i,j].upper()
							list_of_boards.append(temp)
				except IndexError as e:
					pass
				try:
					if board[i,j+1] == '0':
						temp = board.copy()
						temp[i,j+1] = board[i,j]
						temp[i,j] = temp[i,j].upper()
						list_of_boards.append(temp)
				except IndexError as e:
					pass
				colour_to_look_for.remove(board[i,j])
	return(list_of_boards)

if __name__ == '__main__':
	main()