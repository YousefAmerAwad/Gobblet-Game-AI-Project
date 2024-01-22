import Piece
from Piece import *

class Board:
    def __init__(self, PlayerW, PlayerB):
        self.PlayerW = PlayerW
        self.PlayerB = PlayerB
        self.GBoard = [[[],[],[],[]],
                      [[],[],[],[]],
                      [[],[],[],[]],
                      [[],[],[],[]]]
        for y in range(4):
            for x in range(4):
                self.GBoard[y][x].append(Piece("X", -1))
        
        self.currentPlayer = self.PlayerW
    def showBoard(self):
        for y in range(4):
            print("["+ str(self.pieceAt(0,y).Size)+self.pieceAt(0,y).Color+"]"+"["+ str(self.pieceAt(1,y).Size)+self.pieceAt(1,y).Color+"]"+"["+ str(self.pieceAt(2,y).Size)+self.pieceAt(2,y).Color+"]"+"["+ str(self.pieceAt(3,y).Size)+self.pieceAt(3,y).Color+"]")
    def nextTurn(self):
        if (self.currentPlayer.Color=='W'):
            self.currentPlayer = self.PlayerB
        elif (self.currentPlayer.Color=='B'):
            self.currentPlayer = self.PlayerW

    def move(self, piece, x, y):
        if (piece.Color!=self.currentPlayer.Color):
            return False
        if (self.pieceAt(x, y).Size < piece.Size):
            self.GBoard[y][x].append(piece)
            return True
        return False
    
    def movFromBoard(self, piece, x, y):
        return self.move(piece, x, y)
    
    def movFromInv(self, piece, x, y):
        if (self.pieceAt(x,y).Size==-1):
            if (self.move(piece, x, y)):
                self.currentPlayer.removePiece(piece)
                return True
            return False
        elif(self.partOf3Rule(x,y,piece)):
            self.move(piece, x, y)
            self.currentPlayer.removePiece(piece)
            return True
        return False
    
    def grabFromBoard(self, x, y):
        return self.GBoard[y][x].pop()


    def checkWin(self, color):

        for r in range(4):
            if (self.pieceAt(0,r).Color==color and
                self.pieceAt(1,r).Color==color and
                self.pieceAt(2,r).Color==color and
                self.pieceAt(3,r).Color==color):
                return True

        for c in range(4):
            if (self.pieceAt(c,0).Color==color and
                self.pieceAt(c,1).Color==color and
                self.pieceAt(c,2).Color==color and
                self.pieceAt(c,3).Color==color):
                return True

        if (self.pieceAt(0,0).Color==color and
            self.pieceAt(1,1).Color==color and
            self.pieceAt(2,2).Color==color and
            self.pieceAt(3,3).Color==color):
            return True
        if (self.pieceAt(3,0).Color==color and
            self.pieceAt(2,1).Color==color and
            self.pieceAt(1,2).Color==color and
            self.pieceAt(0,3).Color==color):
            return True
        return False

    def pieceAt(self, x, y):
        return self.GBoard[y][x][len(self.GBoard[y][x])-1]
    def piecesAt(self, x, y):
        return self.GBoard[y][x]

    def partOf3Rule(self, x, y, piece):
        if (self.pieceAt(x,y).Color == self.currentPlayer.Color):
            return False
        if (self.pieceAt(x,y).Size>=piece.Size):
            return False
        return self.partOf3NS(x,y) or self.partOf3WE(x,y) or self.partOf3NW(x,y) or self.partOf3NE(x,y)


    def partOf3NS(self, x, y):
        color = self.pieceAt(x,y).Color
        top = False
        mid = False
        bot = False
        if (y==0):
            top = self.pieceAt(x,y+1).Color==color and self.pieceAt(x,y+2).Color==color
        if (y==1):
            top = self.pieceAt(x,y+1).Color==color and self.pieceAt(x,y+2).Color==color
            mid = self.pieceAt(x,y+1).Color==color and self.pieceAt(x,y-1).Color==color
        if (y==2):
            mid = self.pieceAt(x,y+1).Color==color and self.pieceAt(x,y-1).Color==color
            bot = self.pieceAt(x,y-1).Color==color and self.pieceAt(x,y-2).Color==color
        if (y==3):
            bot = self.pieceAt(x,y-1).Color==color and self.pieceAt(x,y-2).Color==color
        return top or mid or bot
    def partOf3WE(self, x, y):
        color = self.pieceAt(x,y).Color
        left = False
        mid = False
        right = False
        if (x==0):
            left = self.pieceAt(x+1,y).Color==color and self.pieceAt(x+2,y).Color==color
        if (x==1):
            left = self.pieceAt(x+1,y).Color==color and self.pieceAt(x+2,y).Color==color
            mid = self.pieceAt(x+1,y).Color==color and self.pieceAt(x-1,y).Color==color
        if (x==2):
            right = self.pieceAt(x-1,y).Color==color and self.pieceAt(x-2,y).Color==color
            mid = self.pieceAt(x+1,y).Color==color and self.pieceAt(x-1,y).Color==color
        if (x==3):
            right = self.pieceAt(x-1,y).Color==color and self.pieceAt(x-2,y).Color==color
        return left or mid or right
    def partOf3NW(self, x, y):
        color = self.pieceAt(x,y).Color
        topleft = False
        mid = False
        botright = False
        if (y==0):
            if (x==0 or x==1):
                topleft = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x+2,y+2).Color==color
        if (y==1):
            if (x==1):
                topleft = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x+2,y+2).Color==color
                mid = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x-1,y-1).Color==color
            if (x==0):
                topleft = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x+2,y+2).Color==color
            if (x==2):
                mid = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x-1,y-1).Color==color
        if (y==2):
            if (x==1):
                mid = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x-1,y-1).Color==color
            if (x==2):
                mid = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x-1,y-1).Color==color
                botright = self.pieceAt(x-1,y-1).Color==color and self.pieceAt(x-2,y-2).Color==color
            if (x==3):
                botright = self.pieceAt(x-1,y-1).Color==color and self.pieceAt(x-2,y-2).Color==color
        if (y==3):
            if (x==2 or x==3):
                botright = self.pieceAt(x-1,y-1).Color==color and self.pieceAt(x-2,y-2).Color==color
        return topleft or mid or botright
    def partOf3NE(self, x, y):
        color = self.pieceAt(x,y).Color
        topright = False
        mid = False
        botleft = False
        if (y==0):
            if (x==2 or x==3):
                topright = self.pieceAt(x-1,y+1).Color==color and self.pieceAt(x-2,y+2).Color==color
        if (y==1):
            if (x==2):
                topright = self.pieceAt(x-1,y+1).Color==color and self.pieceAt(x-2,y+2).Color==color
                mid = self.pieceAt(x-1,y+1).Color==color and self.pieceAt(x+1,y-1).Color==color
            if (x==3):
                topright = self.pieceAt(x-1,y+1).Color==color and self.pieceAt(x-2,y+2).Color==color
            if (x==1):
                mid = self.pieceAt(x-1,y+1).Color==color and self.pieceAt(x+1,y-1).Color==color
        if (y==2):
            if (x==2):
                mid = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x-1,y-1).Color==color
            if (x==1):
                mid = self.pieceAt(x+1,y+1).Color==color and self.pieceAt(x-1,y-1).Color==color
                botleft = self.pieceAt(x-1,y-1).Color==color and self.pieceAt(x-2,y-2).Color==color
            if (x==0):
                botleft = self.pieceAt(x-1,y-1).Color==color and self.pieceAt(x-2,y-2).Color==color
        if (y==3):
            if (x==0 or x==1):
                botleft = self.pieceAt(x-1,y-1).Color==color and self.pieceAt(x-2,y-2).Color==color
        return topright or mid or botleft
