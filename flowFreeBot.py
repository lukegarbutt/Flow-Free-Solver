import pyautogui
import cv2
import numpy
import PIL
import time
#capture the screen
#detect the size of the board
#locate the colours
#solve the array
#drawing the array to the screen
#done

def main():
	pyautogui.PAUSE = 0
	dimensions_of_board = (30, 170, 470, 610)
	original_board = capture_board(dimensions_of_board)
	#cv2.imshow('original_board', original_board)
	#cv2.waitKey(0)
	size_of_board = vertical_line_detector(original_board)
	print('You are playing a {} x {} board'.format(size_of_board, size_of_board))
	size_of_square = (dimensions_of_board[2]-dimensions_of_board[0])/size_of_board
	#centre_of_circles = locate_colours(size_of_board, size_of_square, original_board)
	board_of_pixels = create_pixel_board(dimensions_of_board, size_of_board, size_of_square)
	#print(board_of_pixels)
	board_of_colours = create_colour_board(board_of_pixels, size_of_board)
	solved_board = solveboard(board_of_colours, size_of_board)

	print(solved_board)

	'''solved_check = solved_checker(solved_board, size_of_board)
	if solved_check == False:
		print('solution was not found, best solution was {}'.format(solved_board))
		pyautogui.moveTo(330,650)#skip level
		pyautogui.click()
		time.sleep(1)
		main()'''

	list_of_array_of_moves = move_finder(solved_board, board_of_colours, size_of_board)
	draw_solution(board_of_pixels, list_of_array_of_moves)
	time.sleep(1)
	'''pyautogui.moveTo(250,370)#move to next level
	pyautogui.click() #click next level
	time.sleep(1)'''
	main()

def solved_checker(solved_board, size_of_board):
	for i in range(size_of_board):
		for j in range(size_of_board):
			if solved_board[i,j] == '0':
				return(False)
	return(True)


def draw_solution(board_of_pixels, list_of_array_of_moves):
	for i in range(len(list_of_array_of_moves)):
		current_moves_to_do = list_of_array_of_moves[i]
		move_number = 1
		while(True):
			loc_data = numpy.where(current_moves_to_do == move_number)
			if len(loc_data[0]) == 0:
				break
			row_index = loc_data[0][0]
			col_index = loc_data[1][0]
			x_coord, y_coord = board_of_pixels[row_index, col_index]
			if move_number == 1:
				pyautogui.moveTo(x_coord, y_coord)
			else:
				pyautogui.dragTo(x_coord, y_coord)
			move_number += 1
			#time.sleep(1)
			



def move_finder(solved_board, unsolved_board, size_of_board):
	unsolved_board_with_x = numpy.zeros((size_of_board+2, size_of_board+2), dtype=str)
	for i in range(size_of_board+2):
		for j in range(size_of_board+2):
			unsolved_board_with_x[i,j] = 'x'
	for i in range(size_of_board):
		for j in range(size_of_board):
			unsolved_board_with_x[i+1,j+1] = unsolved_board[i,j]

	solved_board_with_x = numpy.zeros((size_of_board+2, size_of_board+2), dtype=str)
	for i in range(size_of_board+2):
		for j in range(size_of_board+2):
			solved_board_with_x[i,j] = 'x'
	for i in range(size_of_board):
		for j in range(size_of_board):
			solved_board_with_x[i+1,j+1] = solved_board[i,j]

	colours_in_board = []
	list_of_array_of_moves = []
	for i in range(1,size_of_board+1):
		for j in range(1,size_of_board+1):
			if unsolved_board_with_x[i,j] not in (colours_in_board):
				colours_in_board.append(unsolved_board_with_x[i,j])
	colours_in_board.remove('0')

	for colour in colours_in_board:
		colour = colour.upper()
		number_of_colour = 1
		for i in range(1,size_of_board+1):
			for j in range(1,size_of_board+1):
				if solved_board_with_x[i,j] == colour:
					#count the number of that colour in the board
					number_of_colour += 1

		list_of_index = list(range(1, number_of_colour))

		array_of_moves = numpy.zeros((size_of_board, size_of_board), dtype=int)
		for i in range(size_of_board):
			for j in range(size_of_board):
				if unsolved_board_with_x[i+1,j+1] == colour.lower():
					if list_of_index[0] == 1:
						array_of_moves[i,j] = list_of_index.pop(0)
						solved_board_with_x[i+1,j+1] = '0'
					else:
						array_of_moves[i,j] = list_of_index.pop(-1)
						solved_board_with_x[i+1,j+1] = '0'

		while((len(list_of_index)) > 0):
			for i in range(1,size_of_board+1):
				for j in range(1,size_of_board+1):
					#print(array_of_moves)
					if array_of_moves[i-1,j-1] == list_of_index[0]-1 or array_of_moves[i-1,j-1] == list_of_index[-1]+1:
						#we have found an 'end' now we must check if it's move is forced

						#check if moving right is forced
						if solved_board_with_x[i-1,j] != colour and solved_board_with_x[i,j-1] != colour and solved_board_with_x[i+1,j] != colour and solved_board_with_x[i,j+1] == colour:
							if list_of_index[0]-1 == array_of_moves[i-1,j-1]:
								array_of_moves[i-1,j] = list_of_index.pop(0)
								solved_board_with_x[i,j] = '0'
							else:
								array_of_moves[i-1,j] = list_of_index.pop(-1)
								solved_board_with_x[i,j] = '0'

						#check if moving left is forced
						if solved_board_with_x[i-1,j] != colour and solved_board_with_x[i,j-1] == colour and solved_board_with_x[i+1,j] != colour and solved_board_with_x[i,j+1] != colour:
							if list_of_index[0]-1 == array_of_moves[i-1,j-1]:
								array_of_moves[i-1,j-2] = list_of_index.pop(0)
								solved_board_with_x[i,j] = '0'
							else:
								array_of_moves[i-1,j-2] = list_of_index.pop(-1)
								solved_board_with_x[i,j] = '0'

						#check if moving up is forced
						if solved_board_with_x[i-1,j] == colour and solved_board_with_x[i,j-1] != colour and solved_board_with_x[i+1,j] != colour and solved_board_with_x[i,j+1] != colour:
							if list_of_index[0]-1 == array_of_moves[i-1,j-1]:
								array_of_moves[i-2,j-1] = list_of_index.pop(0)
								solved_board_with_x[i,j] = '0'
							else:
								array_of_moves[i-2,j-1] = list_of_index.pop(-1)
								solved_board_with_x[i,j] = '0'

						#check if moving down is forced
						if solved_board_with_x[i-1,j] != colour and solved_board_with_x[i,j-1] != colour and solved_board_with_x[i+1,j] == colour and solved_board_with_x[i,j+1] != colour:
							if list_of_index[0]-1 == array_of_moves[i-1,j-1]:
								array_of_moves[i,j-1] = list_of_index.pop(0)
								solved_board_with_x[i,j] = '0'
							else:
								array_of_moves[i,j-1] = list_of_index.pop(-1)
								solved_board_with_x[i,j] = '0'
					if (len(list_of_index)) == 0:
						break
				if (len(list_of_index)) == 0:
					break
		list_of_array_of_moves.append(array_of_moves)
	return(list_of_array_of_moves)

def solveboard(unsolved_board, size_of_board):
	characters_that_are_ends = ['b', 'r', 'g', 'y', 'o', 'p', 'z', 'c', 't', 'd', 'q', 's', 'l', 'm', 'w', 'a']
	original_unsolved_board = unsolved_board
	unsolved_board = forced_move_check(unsolved_board, size_of_board, characters_that_are_ends)
	if not numpy.array_equal(original_unsolved_board, unsolved_board):
		unsolved_board = solveboard(unsolved_board, size_of_board)
	#try next solve method
	unsolved_board = corner_move_check(unsolved_board, size_of_board, characters_that_are_ends)
	if not numpy.array_equal(original_unsolved_board, unsolved_board):
		unsolved_board = solveboard(unsolved_board, size_of_board)

	return(unsolved_board)

def corner_move_check(unsolved_board, size_of_board, characters_that_are_ends):
	if unsolved_board[size_of_board-2, 0] in characters_that_are_ends and unsolved_board[size_of_board-1,0] == '0':
		unsolved_board[size_of_board-1, 0] = unsolved_board[size_of_board-2, 0]
		unsolved_board[size_of_board-2, 0] = numpy.core.defchararray.capitalize(unsolved_board[size_of_board-2, 0])
	elif unsolved_board[size_of_board-1, 1] in characters_that_are_ends and unsolved_board[size_of_board-1,0] == '0':
		unsolved_board[size_of_board-1, 0] = unsolved_board[size_of_board-1, 1]
		unsolved_board[size_of_board-1, 1] = numpy.core.defchararray.capitalize(unsolved_board[size_of_board-1, 1])

	elif unsolved_board[1, 0] in characters_that_are_ends and unsolved_board[0,0] == '0':
		unsolved_board[0, 0] = unsolved_board[1, 0]
		unsolved_board[1, 0] = numpy.core.defchararray.capitalize(unsolved_board[1, 0])
	elif unsolved_board[0, 1] in characters_that_are_ends and unsolved_board[0,0] == '0':
		unsolved_board[0, 0] = unsolved_board[0, 1]
		unsolved_board[0, 1] = numpy.core.defchararray.capitalize(unsolved_board[0, 1])

	elif unsolved_board[0, size_of_board-2] in characters_that_are_ends and unsolved_board[0,size_of_board-1] == '0':
		unsolved_board[0, size_of_board-1] = unsolved_board[0, size_of_board-2]
		unsolved_board[0, size_of_board-2] = numpy.core.defchararray.capitalize(unsolved_board[0, size_of_board-2])
	elif unsolved_board[1, size_of_board-1] in characters_that_are_ends and unsolved_board[0,size_of_board-1] == '0':
		unsolved_board[0, size_of_board-1] = unsolved_board[1, size_of_board-1]
		unsolved_board[1, size_of_board-1] = numpy.core.defchararray.capitalize(unsolved_board[1, size_of_board-1])

	elif unsolved_board[size_of_board-2, size_of_board-1] in characters_that_are_ends and unsolved_board[size_of_board-1,size_of_board-1] == '0':
		unsolved_board[size_of_board-1, size_of_board-1] = unsolved_board[size_of_board-2, size_of_board-1]
		unsolved_board[size_of_board-2, size_of_board-1] = numpy.core.defchararray.capitalize(unsolved_board[size_of_board-2, size_of_board-1])
	elif unsolved_board[size_of_board-1, size_of_board-2] in characters_that_are_ends and unsolved_board[size_of_board-1,size_of_board-1] == '0':
		unsolved_board[size_of_board-1, size_of_board-1] = unsolved_board[size_of_board-1, size_of_board-2]
		unsolved_board[size_of_board-1, size_of_board-2] = numpy.core.defchararray.capitalize(unsolved_board[size_of_board-1, size_of_board-2])

	return(unsolved_board)

def forced_move_check(unsolved_board, size_of_board, characters_that_are_ends):
	board_with_x = numpy.zeros((size_of_board+2, size_of_board+2), dtype=str)
	for i in range(size_of_board+2):
		for j in range(size_of_board+2):
			board_with_x[i,j] = 'x'
	for i in range(size_of_board):
		for j in range(size_of_board):
			board_with_x[i+1,j+1] = unsolved_board[i,j]

	for i in range(1, size_of_board+1):
		for j in range(1, size_of_board+1):
			
			#check for any lone ends
			for colour in characters_that_are_ends:
				colour_count = 0
				for k in range(1, size_of_board+1):
					for l in range(1, size_of_board+1):
						if colour == board_with_x[k,l]:
							colour_count += 1

				#capitalize any lone ends
				if colour_count == 1:
					for k in range(1, size_of_board+1):
						for l in range(1, size_of_board+1):
							if colour == board_with_x[k,l]:
								board_with_x[k,l] = numpy.core.defchararray.capitalize(board_with_x[k,l])
		
			#check if we are forced to move right
			if board_with_x[i,j] in characters_that_are_ends:
				if board_with_x[i-1,j] not in ('0', board_with_x[i,j]) and board_with_x[i,j-1] not in ('0', board_with_x[i,j]) and board_with_x[i+1,j] not in ('0', board_with_x[i,j]) and board_with_x[i,j+1] in ('0', board_with_x[i,j]):
					board_with_x[i,j+1] = board_with_x[i,j]
					board_with_x[i,j] = numpy.core.defchararray.capitalize(board_with_x[i,j])

			#check if we are forced to move left
				elif board_with_x[i-1,j] not in ('0', board_with_x[i,j]) and board_with_x[i,j-1] in ('0', board_with_x[i,j]) and board_with_x[i+1,j] not in ('0', board_with_x[i,j]) and board_with_x[i,j+1] not in ('0', board_with_x[i,j]):
					board_with_x[i,j-1] = board_with_x[i,j]
					board_with_x[i,j] = numpy.core.defchararray.capitalize(board_with_x[i,j])

			#check if we are forced to move up
				elif board_with_x[i-1,j] in ('0', board_with_x[i,j]) and board_with_x[i,j-1] not in ('0', board_with_x[i,j]) and board_with_x[i+1,j] not in ('0', board_with_x[i,j]) and board_with_x[i,j+1] not in ('0', board_with_x[i,j]):
					board_with_x[i-1,j] = board_with_x[i,j]
					board_with_x[i,j] = numpy.core.defchararray.capitalize(board_with_x[i,j])

			#check if we are forced to move down
				elif board_with_x[i-1,j] not in ('0', board_with_x[i,j]) and board_with_x[i,j-1] not in ('0', board_with_x[i,j]) and board_with_x[i+1,j] in ('0', board_with_x[i,j]) and board_with_x[i,j+1] not in ('0', board_with_x[i,j]):
					board_with_x[i+1,j] = board_with_x[i,j]
					board_with_x[i,j] = numpy.core.defchararray.capitalize(board_with_x[i,j])
	
	board_to_return = numpy.zeros((size_of_board,size_of_board), dtype=str)
	for i in range(size_of_board):
		for j in range(size_of_board):
			board_to_return[i,j] = board_with_x[i+1,j+1]
	return(board_to_return)

def create_colour_board(board_of_pixels, size_of_board):
	dict_of_colours = {(0,0,255):'b', (255,0,0):'r', (0,128,0):'g', (238,238,0):'y', (255,127,0):'o', (255,0,255):'p',
						(128,0,128):'z', (0,255,255):'c', (0,128,128):'t', (0,0,139):'d', (166,166,166):'q',
						(189,183,107):'s', (0,255,0):'l', (165,42,42):'m', (255,255,255):'w', (128,128,128):'a'}
	board_of_colours = numpy.zeros((size_of_board, size_of_board), dtype = str)
	for i in range(size_of_board):
		for j in range(size_of_board):
			if pyautogui.pixel(board_of_pixels[i,j][0],board_of_pixels[i,j][1]) in dict_of_colours.keys():
				board_of_colours[i,j] = dict_of_colours[pyautogui.pixel(board_of_pixels[i,j][0],board_of_pixels[i,j][1])]
			else:
				board_of_colours[i,j] = '0'
	return(board_of_colours)

def create_pixel_board(dimensions_of_board, size_of_board, size_of_square):
	x_dim, y_dim = dimensions_of_board[0:2]
	board_of_pixels = numpy.zeros((size_of_board, size_of_board), dtype = object)
	for i in range(size_of_board):
		for j in range(size_of_board):
			board_of_pixels[i,j] = (int(x_dim + j*size_of_square + 0.5*size_of_square),
									int(y_dim + i*size_of_square + 0.5*size_of_square))
	return(board_of_pixels)

def capture_board(dimensions_of_board):
	image_of_board = numpy.array(PIL.ImageGrab.grab(bbox=(dimensions_of_board)))
	image_of_board = cv2.cvtColor(image_of_board, cv2.COLOR_BGR2RGB)
	return(image_of_board)

def vertical_line_detector(image):
	line_tolerance = 5
	gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	edge_image = cv2.Canny(gray_image, threshold1 = 100, threshold2 = 200, apertureSize = 3)
	lines = cv2.HoughLinesP(image=edge_image, rho=1, theta=numpy.pi, threshold=100, 
							lines=numpy.array([]), minLineLength=400,maxLineGap=5)
	holder1 = -1
	for line1 in lines:
		holder1 += 1
		holder2 = -1
		for line2 in lines:
			holder2 += 1
			if line1[0][0] < line2[0][0] and line1[0][0] + line_tolerance > line2[0][0]:
				lines = numpy.delete(lines, holder2, 0)
	return(len(lines)-1)

def locate_colours(size_of_board, size_of_square, image):
	minradius = int((430/size_of_board)*0.3)
	maxradius = int((430/size_of_board)*0.5)
	mindist = int((430/size_of_board)*0.1)
	edge_image = cv2.Canny(image, threshold1 = 100, threshold2 = 200, apertureSize = 3)
	blurred_image = cv2.GaussianBlur(edge_image, (5,5), 0)
	circles = cv2.HoughCircles(blurred_image, cv2.HOUGH_GRADIENT, 14.5, mindist, param1 = 100, param2=400, minRadius=minradius, maxRadius=maxradius)
	circles = numpy.round(circles[0, :]).astype("int")
	centre_of_circles = []
	for i in circles:
		centre_of_circles.append(list(i[0:2]))
	return(centre_of_circles)
	'''for i in range(len(centre_of_circles)):
		centre_of_circles[i][0] = centre_of_circles[i][0] + x_dim
		centre_of_circles[i][1] = centre_of_circles[i][1] + y_dim'''





main()
