array = [] #Defines empty array

for i in range(10):			# for numbers 0-9 (number of rows)
	column = []				# define a column for each row
	for j in range(10):		# enters each element of the current column
		column.append(j)	# inserts new element with value j to the end of the column array
	array.append(column)	# inserts new column array to the end of the row array

for row in array:					# for each row in array
	for element in row:				# for each element in row
		print(element, end = ' ')	# print the value and a space
	print(end = "\n")				# print a new line after every column


def add_to_array(value, my_array):		# define method to add a value to every element in array
	for row in my_array:				# for each row in array
		for element in row:				# for each element in row
			element =  element + value	# set element to element plus value



def print_array(my_array):				# define method to print an array
	print('_' * 20)						# print 20 underscores
	for row in my_array:				# for each row in array 
		for element in row:				# for each element in row
			print(element, end = ' ')	# print the value and a space
		print()							# print a new line after every column


add_to_array(10, array)

print_array(array)


