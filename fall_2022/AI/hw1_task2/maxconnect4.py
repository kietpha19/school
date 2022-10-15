#!/usr/bin/env python

# Written by Chris Conly based on C++
# code provided by Dr. Vassilis Athitsos
# Originally, written to be Python 2.4 compatible for omega
# Modified by student, Hoang Anh Kiet PHam, to be Python 3.8.10 compatible for omage

from cmath import inf
import sys
from MaxConnect4Game import *

def print_currentGame(currentGame):
    currentGame.printGameBoard()
    # Update a few game variables based on initial state and print the score
    currentGame.checkPieceCount()
    currentGame.countScore()
    print('Score: Player 1 = %d, Player 2 = %d\n' % (currentGame.player1Score, currentGame.player2Score))

    if currentGame.pieceCount == 42:    # Is the board full already?
        print('BOARD FULL\n\nGame Over!\n')
        sys.exit(0)

def oneMoveGame(currentGame, depth):
    currentGame.process_input_file()
    currentGame.gameInFile.close()
    
    print ('Game state before move:')
    print_currentGame(currentGame)

    currentGame.aiPlay(depth) # Make a move

    currentGame.printGameBoardToFile()
    currentGame.gameOutFile.close()

    print( 'Game state after move:')
    print_currentGame(currentGame)


def interactiveGame(currentGame, next_player, depth):
    print_currentGame(currentGame)

    if next_player == "computer-next":
        print("AI play")
        currentGame.aiPlay(depth)
        
        try:
            currentGame.gameOutFile = open("computer.txt", 'w')
        except:
            sys.exit('Error opening output file.')
        currentGame.printGameBoardToFile()
        currentGame.gameOutFile.close()

        interactiveGame(currentGame, "human-next", depth)
    
    else: #next_player == "human-next"
        c = input("pick a column: ")
        if c == 'q':
            sys.exit(0)
        else:
            c = int(c)
        while(c<1 or c>7 or currentGame.playPiece(c-1) == None):
            c = input("in valid move, try again: ")
            if c == 'q':
                sys.exit(0)
            else:
                c = int(c)
        
        try:
            currentGame.gameOutFile = open("human.txt", 'w')
        except:
            sys.exit('Error opening output file.')
        print('move %d: Player %d, column %d' %(currentGame.pieceCount, currentGame.currentTurn, c))

        currentGame.currentTurn = (currentGame.currentTurn%2) + 1
        currentGame.printGameBoardToFile()
        currentGame.gameOutFile.close()
 
        interactiveGame(currentGame, "computer-next", depth)

    
def main(argv):
    # Make sure we have enough command-line arguments
    if len(argv) != 5:
        print( 'Four command-line arguments are needed:')
        print('Usage: %s interactive [input_file] [computer-next/human-next] [depth]' % argv[0])
        print('or: %s one-move [input_file] [output_file] [depth]' % argv[0])
        sys.exit(2)

    game_mode, inFile = argv[1:3]

    if not game_mode == 'interactive' and not game_mode == 'one-move':
        print('%s is an unrecognized game mode' % game_mode)
        sys.exit(2)

    currentGame = maxConnect4Game() # Create a game
    print ('\nMaxConnect-4 game\n')

    if game_mode == 'interactive':
        next_player = argv[3]
        if next_player != "computer-next" and next_player != "human-next":
            print('%s is an unrecognized next player' % next_player)
            sys.exit(2)
        #try process the input file
        try:
            currentGame.gameInFile = open(inFile, 'r')
            currentGame.process_input_file()
            currentGame.gameInFile.close()
        except:
            print("file read errors, start new game")
        depth = int(argv[4])
        interactiveGame(currentGame, next_player, depth) # Be sure to pass whatever else you need from the command line
    
    else: # game_mode == 'one-move'
        #try open the input file
        try:
            currentGame.gameInFile = open(inFile, 'r')
        except IOError:
            sys.exit("\nError opening input file.\nCheck file name.\n")
            
        #try open the output file
        outFile = argv[3]
        try:
            currentGame.gameOutFile = open(outFile, 'w')
        except:
            sys.exit('Error opening output file.')

        depth = int(argv[4])
        oneMoveGame(currentGame, depth) # Be sure to pass any other arguments from the command line you might need.


if __name__ == '__main__':
    main(sys.argv)



