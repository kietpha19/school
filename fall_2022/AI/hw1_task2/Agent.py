from MaxConnect4Game import *

class Agent:
    def __init__(self, gameBoard, currentTurn, depth):
        self.depth = depth
        self.gameBoard = gameBoard
        self.currentTurn = currentTurn

    def predict(self):
        self.gameBoard[0][1] = 3
        self.currentTurn = 3
        print(self.gameBoard)
        print(self.currentTurn)
        return 1;