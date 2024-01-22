from Piece import *

class Player:
    def __init__(self, BorW, Name):
        self.Name = Name
        self.Color = BorW
        self.Inv = [[],[],[]]
        for x in range(3):
            for z in range(4):
                self.Inv[x].append(Piece(self.Color, z))
    def ShowInv(self):
        for i in range(3):
            print('stack number ' + str(i+1) + ': ')
            stack = self.Inv[i]
            slen = len(stack)
            for i in range(slen):
                print(stack[slen-i-1].Color + str(stack[slen-i-1].Size))

    def getTopPiece(self, stacknum):
        stack = self.Inv[stacknum-1]
        if (len(stack)==0):
            return Piece('X', -1)
        return stack[len(stack)-1]

    def removePiece(self, piece):
        for i in range(3):
            stack = self.Inv[i]
            if (len(stack)==0):
                pass
            elif (stack[len(stack)-1]==piece):
                self.Inv[i] = stack[:len(stack)-1]
                return piece
        return piece
