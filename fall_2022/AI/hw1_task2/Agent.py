#from asyncio.windows_events import INFINITE
from cmath import inf
from inspect import currentframe
from MaxConnect4Game import *

class Agent:
    action = 0
    def __init__(self, currentGame, depth):
        self.depth = depth
        self.currentGame = currentGame

    def predict(self):
        self.minimax(self.currentGame, self.depth, -inf, inf, self.currentGame.currentTurn)
        #print("action: ", self.action)
        return self.action

    def minimax(self, currentGame, depth, alpha, beta, player):
        # currentGame.printGameBoard()
        # print(currentGame.pieceCount)
        if(currentGame.pieceCount == 42 or depth == 0):
            return self.eval_function(currentGame)
        
        if player == 1:
            maxEval = -inf
            for c in range(7):
                child_game = currentGame.make_a_copy()
                if child_game.playPiece(c) != None:
                    child_game.currentTurn = 2
                    eval = self.minimax(child_game, depth-1, alpha, beta, 2)
                    if(depth == self.depth and eval > maxEval):
                        #print("c: ", c)
                        self.action = c
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        self.action = c
                        break
            return maxEval
        else: #player ==2
            minEval = +inf
            for c in range(7):
                child_game = currentGame.make_a_copy()
                if child_game.playPiece(c) != None:
                    child_game.currentTurn = 1
                    eval = self.minimax(child_game, depth-1, alpha, beta, 1)
                    if(depth == self.depth and eval < minEval):
                        #print("c: ", c)
                        self.action = c
                    minEval = min(minEval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return minEval
                    
    
    def eval_function(self, currentGame):
        currentGame.countScore()
        # currentGame.printGameBoard()
        # print("1: ", currentGame.player1Score)
        # print("2: ", currentGame.player2Score)
        return int(currentGame.player1Score) - int(currentGame.player2Score)