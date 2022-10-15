from cmath import inf
from MaxConnect4Game import *

class Agent:
    action = 0
    def __init__(self, currentGame, depth):
        self.depth = depth
        self.currentGame = currentGame

    #this function will call the minimax function
    def predict(self):
        # if(self.currentGame.pieceCount == 0):
        #     return 4

        #alphe is negetive inf and beta is positive inf
        self.minimax(self.currentGame, self.depth, -inf, inf, self.currentGame.currentTurn)
        #print("action: ", self.action)
        return self.action

    def minimax(self, currentGame, depth, alpha, beta, player):
        # currentGame.printGameBoard()
        # print(currentGame.pieceCount)
        if(currentGame.pieceCount == 42 or depth == 0):
            if(currentGame.pieceCount > 25):
                return self.basic_eval_function(currentGame)
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
                    
    #this eval function basically, based all the difference between player 1 score and player 2 score at a given state
    def basic_eval_function(self, currentGame):
        currentGame.countScore()
        # currentGame.printGameBoard()
        # print("1: ", currentGame.player1Score)
        # print("2: ", currentGame.player2Score)
        return int(currentGame.player1Score) - int(currentGame.player2Score)
    
   
    '''
    this function not only take into account of 4 consecute streak, but also count the POSSIBLE streak
    for example, if the is already 3 consecutive and there is empty next to it
    same for 2 and 1
    However, if the max consicutive streak it can make is less than 4, then it will decrease the score (the estimated score at given state)
    '''
    def eval_function(self, currentGame):
        board = currentGame.gameBoard
        player1_score = 0
        player2_score = 0
        for i in range(6):
            for j in range(7):
                if board[i][j] == 1:
                    player1_score += self.count_consecutive(board, [i,j], 1)
                elif board[i][j] == 2:
                    player2_score += self.count_consecutive(board, [i,j], 2)
        # currentGame.printGameBoard()
        # print("1: ", player1_score)
        # print("2: ", player2_score)
        return (player1_score - player2_score)
    
    def count_consecutive(self, board, pos, player):
        score = 0
        score += self.check_horizontal(board, pos, player)
        score += self.check_vertical(board, pos, player)
        score += self.check_diagonal(board, pos, player)
        return score
    
    def check_horizontal(self, board, pos, player):
        i = pos[0]
        j = pos[1]
        streak = 0

        #check to the left
        c = 0
        score = 0
        while j >=0 and board[i][j] == player:
            streak +=1
            c+=1
            j-=1
        while streak != 0 and j>=0 and board[i][j] == 0:
            c+=1
            j-=1
        if c >= 4:
            if streak > 4:
                score += 15*streak
            elif streak == 3:
                score += 10* streak
            elif streak == 2:
                score += 5*streak
            else:
                score += streak
        else:
           score -= 10*streak
        
        #check to the right
        streak = 0
        c = 0
        while j <7 and board[i][j] == player:
            streak +=1
            c+=1
            j+=1
        while streak != 0 and j<7 and board[i][j] == 0:
            c+=1
            j+=1
        if c >= 4:
            if streak > 4:
                score += 15*streak
            elif streak == 3:
                score += 10* streak
            elif streak == 2:
                score += 5*streak
            else:
                score += streak
        else:
            score -= 10*(4-streak)

        return score
    
    def check_vertical(self, board, pos, player):
        i = pos[0]
        j = pos[1]
        streak = 0
        c = 0
        while i>=0 and board[i][j] == player:
            streak +=1
            i-=1
            c+=1
        while streak != 0 and i>=0 and board[i][j] == 0:
            i-=1
            c+=1
        score = 0
        if c>=4:
            if streak > 4:
                score += 20*streak
            elif streak == 3:
                score += 10* streak
            elif streak == 2:
                score += 5*streak
            else:
                score += 2*streak
        else:
           score -= 15*(4-streak)
        return score
    
    def check_diagonal(self, board, pos, player):
        streak = 0

        #top left - bottom right
        i = pos[0]
        j = pos[1]
        while(0 <= i < 6 and 0<= j < 7 and board[i][j] == player):
            streak +=1
            i+=1
            j+=1
        
        #top right = bottom left
        i = pos[0]
        j = pos[1]
        while(0 <= i < 6 and 0<= j < 7 and board[i][j] == player):
            streak +=1
            i+=1
            j-=1
        
        return 7*streak if streak>=4 else 7*(streak-4)
