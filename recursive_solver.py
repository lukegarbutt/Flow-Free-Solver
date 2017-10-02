# This will be a brute force attempt at solving the game, with the hope of being able to add this as a final resort to solve boards
import flowFreeBot
import numpy
import time
import pyautogui

# we need a way to see if a solution is found, and also need to define constraints so we know when we have found an invalid state
# then we need to initialise the board and find the initial gamestate
# we now save this as the top of our tree
# once we have this we make a random move
# then we check if our new gamestate is valid, if so we add this one layer down on our tree
# we repeat until one of two things happens..
# a) we solve the board and so are done
# b) we reach an invalid state, in which case we backtrack one level in the tree and try to take a different path
# if no other paths are possible we go up another level
# eventually we should reach a solution

def test():
	board = numpy.array([['0', '0', '0', '0', '0'],
						['0', 'r', '0', 'r', '0'],
						['0', '0', '0', '0', 'b'],
						['b', '0', 'g', '0', 'y'],
						['y', '0', '0', '0', 'g']])
	'''board = numpy.array([['r', '0', '0', '0', 'r'],
						['b', '0', 'b', 'B', 'B'],
						['B', '0', '0', '0', 'B'],
						['B', '0', 'g', '0', 'y'],
						['y', '0', '0', '0', 'g']])'''
	print(recurse_solve(board))


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
		solved_board = recurse_solve(board_of_colours)
		print(solved_board)
		list_of_array_of_moves = flowFreeBot.move_finder(solved_board, board_of_colours, size_of_board)
		flowFreeBot.draw_solution(board_of_pixels, list_of_array_of_moves)
		time.sleep(1)
		pyautogui.moveTo(250,370)#move to next level
		pyautogui.click() #click next level
		time.sleep(1)
		break

def recurse_solve(board):
	#print(board)
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
	if is_solved(board):
		return(board)
	elif pass_constraints_check(board):
		for possible_board in find_possible_moves(board):
			temp = recurse_solve(possible_board)
			if temp is not None:
				return temp

def find_possible_moves(board): # this will take in a board and returna list of all the possible boards this one could be in 1 move
	characters_that_are_ends = ['b', 'r', 'g', 'y', 'o', 'p', 'z', 'c', 't', 'd', 'q', 's', 'l', 'm', 'w', 'a']
	list_of_boards = []
	for i in range(board.shape[0]):
		for j in range(board.shape[0]):
			if board[i,j] in characters_that_are_ends:
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
				characters_that_are_ends.remove(board[i,j])
	return(list_of_boards)

def is_solved(board): # takes in a board and tells you if it is solved
	elements_in_board = numpy.unique(board)
	if '0' in elements_in_board:
		return(False)
	for colour in elements_in_board:
		number_of_ends = 0
		for i in range(board.shape[0]):
			for j in range(board.shape[1]):
				if board[i,j] == colour:
					adjacent_colours = number_of_neighbours(board, i, j)
					if adjacent_colours == 1:
						number_of_ends += 1
					elif adjacent_colours == 0:
						return(False)
		if number_of_ends != 2:
			return(False)
	return(True)

def pass_constraints_check(board):
	characters_that_are_ends = ['b', 'r', 'g', 'y', 'o', 'p', 'z', 'c', 't', 'd', 'q', 's', 'l', 'm', 'w', 'a']
	for i in range(board.shape[0]):
		for j in range(board.shape[1]):
			if board[i,j] in characters_that_are_ends:
				if number_of_neighbours(board, i, j) > 2:
					return(False) # this is because we have some 'loops' on our board and these are not allowed
	if not impossible_groups_check(board):
		return(False) # this is because we failed the impossible groups check
	return(True)
	# this will check if the board passes all the required constraints with the hope of improving efficiency
	# examples of which are no loops, so all colours must only be adjacent to 1 or 2 of the same colour
	# bottleneck check perhaps
	# this function may not be necessary but should help improve speed

def impossible_groups_check(board):
	characters_that_are_ends = ['b', 'r', 'g', 'y', 'o', 'p', 'z', 'c', 't', 'd', 'q', 's', 'l', 'm', 'w', 'a']
	# this will take in the board and isolate empty spaces into 'groups'
	# it will then check if all of these groups are connected to at least 1 colour with 2 ends in it, else return false
	# it will also check that there are no colours without both its ends in at least one group, else return false
	# failing both of these it will return true
	# This method will group together the empty spaces and check what ends the groups have access to. If a group only has access to both ends of a single colour, then that colour must be the one 
	# to fill the empty space
	group_array = numpy.zeros((board.shape[0], board.shape[1]), dtype=int)
	x = 1
	for i in range(board.shape[0]): # this section creates a new array where groups of empty zones are numbered
		for j in range(board.shape[1]):
			if board[i,j] == '0':
				group_array[i,j] = x
				x += 1
	# next we need to have all the individual groups have unique numbers
	# to do this we will make each group take the same number as the lowest number in its group
	old_array = group_array.copy()
	while(True):
		for i in range(board.shape[0]):
			for j in range(board.shape[1]):
				try:
					if i > 0:
						if group_array[i,j] > group_array[i-1,j] and group_array[i-1,j] != 0:
							group_array[i,j] = group_array[i-1,j]
				except IndexError as e:
					pass
				try:
					if group_array[i,j] > group_array[i+1,j] and group_array[i+1,j] != 0:
						group_array[i,j] = group_array[i+1,j]
				except IndexError as e:
					pass
				try:
					if group_array[i,j] > group_array[i,j+1] and group_array[i,j+1] != 0:
						group_array[i,j] = group_array[i,j+1]
				except IndexError as e:
					pass	
				try:
					if j > 0:
						if group_array[i,j] > group_array[i,j-1] and group_array[i,j-1] != 0:
							group_array[i,j] = group_array[i,j-1]
				except IndexError as e:
					pass
		if numpy.array_equal(old_array, group_array):
			break
		else:
			old_array = group_array.copy()
	group_numbers = [] # this will be a list containing the id's of each of the groups
	for number in numpy.unique(group_array):
		if number != 0:
			group_numbers.append(number)
	elements_in_board = numpy.unique(board)
	colours_in_board = []
	for element in  elements_in_board:
		if element in characters_that_are_ends:
			colours_in_board.append(element)
	for group_id in group_numbers:
		connected_ends = []
		temp_unsolved_board = board.copy()
		for i in range(board.shape[0]):
			for j in range(board.shape[1]):
				if group_array[i,j] == group_id:
					try:
						if i>0:
							if temp_unsolved_board[i-1,j] in characters_that_are_ends:
								connected_ends.append(temp_unsolved_board[i-1,j])
								temp_unsolved_board[i-1,j] = None
					except IndexError as e:
						pass
					try:
						if temp_unsolved_board[i+1,j] in characters_that_are_ends:
							connected_ends.append(temp_unsolved_board[i+1,j])
							temp_unsolved_board[i+1,j] = None
					except IndexError as e:
						pass
					try:
						if j>0:
							if temp_unsolved_board[i,j-1] in characters_that_are_ends:
								connected_ends.append(temp_unsolved_board[i,j-1])
								temp_unsolved_board[i,j-1] = None
					except IndexError as e:
						pass	
					try:
						if temp_unsolved_board[i,j+1] in characters_that_are_ends:
							connected_ends.append(temp_unsolved_board[i,j+1])
							temp_unsolved_board[i,j+1] = None
					except IndexError as e:
						pass
		colours_with_2_ends_connected = []
		for end in connected_ends[::-1]:
			if connected_ends.count(end) > 1:
				colours_with_2_ends_connected.append(end)
				connected_ends.remove(end)
		if len(colours_with_2_ends_connected)<1:
			return(False) # this is because all groups must have at least 1 colours with both ends connected to it
		for colour in colours_with_2_ends_connected:
			if colour in colours_in_board:
				colours_in_board.remove(colour)
	if len(colours_in_board) > 0:
		return(False) # this is because all colours must have at least 1 group that both its ends are connected to
	return(True)

def number_of_neighbours(board, x, y):
	# this will check how many neighbours the x,y square has of the same colour and return it as an int
	number_of_neighbours = 0
	try:
		if x > 0:
			if board[x-1,y].lower() == board[x,y].lower():
				number_of_neighbours += 1
	except IndexError as e:
		pass
	try:
		if board[x+1,y].lower() == board[x,y].lower():
			number_of_neighbours += 1
	except IndexError as e:
		pass
	try:
		if y > 0:
			if board[x,y-1].lower() == board[x,y].lower():
				number_of_neighbours += 1
	except IndexError as e:
		pass
	try:
		if board[x,y+1].lower() == board[x,y].lower():
			number_of_neighbours += 1
	except IndexError as e:
		pass
	return(number_of_neighbours)

start = time.time()
if __name__ == '__main__':
	main()
print('time taken was {} seconds'.format(time.time()-start))