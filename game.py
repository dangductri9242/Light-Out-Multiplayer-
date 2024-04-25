import random

#This is the class represent for the consistent Game of two players.

class GameIn:
    def __init__(self, id):
        NUMBER_OF_ROWS = 10 
        NUMBER_OF_COLS = 20 
        self.p1Went = False # boolean check if player 1 has ready or not
        self.p2Went = False # boolean check if player 2 has ready or not
        self.ready = False #boolean check if the game has been ready to launch
        self.id = id # the id of the game
        self.moves = [[],[]] #moves of players
        self.row = NUMBER_OF_ROWS # number of rows
        self.col = NUMBER_OF_COLS # number of columns
        self.board=finalMatrix(generateSetting(self.row,self.col)) #Initailze a random grid that possible to solve

        #For testing winning stage
        # self.board = [[0 for i in range(self.col)] for j in range(self.row)]
        # borad = self.board
        # borad[0][0] = 1
        # borad[0][1] = 1
        # borad[1][0] = 1
        
    #return the move of the corresponding player
    def get_player_move(self, p):
        return self.moves[p]

    #return the switch light operation
    def switch(self,number):
        if number == 0:
            return 1
        else:
            return 0
        
    #update the board according to the move sent
    def play(self, player, move): #move is a string "row col"

        #Updating move
        self.moves[player].append(move)

        #Set players ready
        if player == 0:
            self.p1Went = True
        else:
            self.p2Went = True

        # Extract the row and col of the move
        moves = list(map(int,move.split()))
        row = moves[1]
        col = moves[0]

        # Updating directly to self.board will cause an error. 
        # Therefore, create a dummy variable, and updating through that dummy variable (thanks to Python)
        boardTempt = self.board

        boardTempt[row][col] = self.switch(boardTempt[row][col])
        if (row-1>=0): 
            boardTempt[row-1][col] = self.switch(boardTempt[row-1][col])
            
        if (row+1<10):
            boardTempt[row+1][col] = self.switch(boardTempt[row+1][col])

        if (col-1>=0):
            boardTempt[row][col-1] = self.switch(boardTempt[row][col-1])

        if (col+1<20):
            boardTempt[row][col+1] = self.switch(boardTempt[row][col+1])
        
    # return the board
    def getBoard(self):
        return self.board
    
    # return if the game is ready or not
    def connected(self):
        return self.ready

    # return if both players are ready or not
    def bothWent(self):
        return self.p1Went and self.p2Went

    # return if have players win yet
    def winner(self):

        board = self.board
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j]==1:
                    return False
        return True
    
# helper method to switch the status of the light
def swap(value):
    if value == 0:
        return 1
    if value == 1:
        return 0
    return value

# helper method to form the answer for the grid. This guarantee that the grid can be always solved if doing in the right way.
def generateSetting(row,col):
    a = []
    for i in range(row):
        tmp = []
        for j in range(col):
            tmp.append(random.randint(0,1))
        a.append(tmp)
    return a

# helper method to finalize the grid
def finalMatrix(setting):
    row=len(setting)
    col=len(setting[0])
    border = [0 for i in range(col)]
    a = []
    for i in range(row):
        tmp = []
        for j in range(col):
            tmp.append(0)
        a.append(tmp)

    for i in range(0,len(setting)):
        for j in range(0,len(setting[i])):
            if setting[i][j]==1:
                a[i][j] = swap(a[i][j])
                if i-1>=0:
                    a[i-1][j] = swap(a[i-1][j])
                if i+1<len(setting):
                    a[i+1][j] = swap(a[i+1][j])
                if j-1>=0:
                    a[i][j-1] = swap(a[i][j-1])
                if j+1<len(setting[i]):
                    a[i][j+1] = swap(a[i][j+1])
    return a

