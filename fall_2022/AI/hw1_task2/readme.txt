Name: Hoang Anh Kiet Pham
UTA ID: 1001904809

Programming Language: python (python3) - UTA virtual machine

CODE STRUCTURE:
	file: maxconnect4.py:
		- this file is a sample code file from the class webpage, handle inputs
		- includes the main function, interactiveGame, and OneMoveGame function
		- was modified a little bit by me to make the code cleaner + add comments

	file: MacConnect4Game.py
		- this file is a sample code file from the class webpage
		- includes class MaxConnect4Game
		- this class is an abstraction of the game board (the board, current turn, players score, piece count, input file and output file)
		- the aiPlay function was modified by me to create an intance of Agent class (later in this class, implement the minimax algorithm),
		- use the agent to pick the column (rather than random origianlly)
	file: Agent.py
		- this file was implemented by myself
		- include class Agents
		- implementation of minimax algorithm and an eval_function based on my ideas (more details are explained along side with code)

COMMANDS TO RUN CODE:
	one move mode: python3 maxconnect4.py one-move <input-file-name> <out-file-name> <depth-limit>
	interactive mode: python3 maxconnect4.py interactive <input-file-name> <human-next / computer-next> <depth-limit>