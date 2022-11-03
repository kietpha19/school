Name: Hoang Anh Kiet Pham
UTA ID: 1001904809

programming language: python (python3) - on UTA virtual machine

CODE STRUCTURE
file name: file_route.py
	class Input:
		- handle all the inputs parameter and files
		fucntion: process_inputFile
			- process the input file and build the graph

	class Graph:
		- path search algorithm
		function print_result + print_route: to print out the output (backtracking)
		fucntion path_search: Uniform cost search algorithm


	class Solution:
		- create instance for 2 classes above and solve search problem
		- all functions are automatically call inside the constructor

#main
create an instance for Solution class

COMMAND TO RUN CODE:
	python3 find_route <input-file-name> <origin-city> <destination> <heuristic-file> 
	notes: the <heuristic-file> is optional
